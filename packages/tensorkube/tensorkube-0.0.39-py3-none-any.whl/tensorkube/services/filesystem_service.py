import json
from typing import Optional

import boto3
import click
import yaml
from kubernetes import config, client, utils
from pkg_resources import resource_filename

from tensorkube.constants import NAMESPACE, REGION, get_efs_service_account_name, get_efs_role_name, get_cluster_name, \
    DEFAULT_NAMESPACE, get_efs_security_group_name
from tensorkube.services.aws_service import get_aws_account_id
from tensorkube.services.eks_service import get_cluster_oidc_issuer_url, get_eks_cluster_vpc_config, get_vpc_cidr, \
    get_security_group_id_by_name
from tensorkube.services.iam_service import delete_iam_role
from tensorkube.services.k8s_service import delete_pvc_using_name_and_namespace, delete_pv_using_name, \
    get_tensorkube_cluster_context_name, get_efs_claim_name


def get_efs_name(cluster_name: str, env: Optional[str] = None):
    if env:
        return f'{cluster_name}-efs-env-{env}'
    return f'{cluster_name}-efs'


def get_efs_pv_name(env: Optional[str] = None):
    if env:
        return f'efs-pv-env-{env}'
    return 'efs-pv'


def get_efs_pvc_name(env: Optional[str] = None):
    if env:
        return f'efs-pvc-env-{env}'
    return 'efs-pvc'


def create_efs_driver_role(account_no: str, role_name: str, oidc_issuer_url: str, namespace: str,
                           service_account_name: str):
    oidc_issuer = oidc_issuer_url[8:]
    region = oidc_issuer.split('.')[2]
    trust_policy_file_path = resource_filename('tensorkube',
                                               'configurations/aws_configs/aws_efs_csi_driver_trust_policy.json')
    with open(trust_policy_file_path, 'r') as f:
        trust_policy = json.load(f)
    trust_policy['Statement'][0]['Principal']['Federated'] = 'arn:aws:iam::{}:oidc-provider/{}'.format(account_no,
                                                                                                       oidc_issuer)
    trust_policy['Statement'][0]['Condition']['StringEquals'] = {
        "{}:sub".format(oidc_issuer): "system:serviceaccount:{}:{}".format(namespace, service_account_name),
        "{}:aud".format(oidc_issuer): "sts.amazonaws.com"}
    iam_client = boto3.client('iam', region_name=region)
    try:
        # Check if the IAM role already exists
        iam_client.get_role(RoleName=role_name)
        print(f"IAM role {role_name} already exists. Skipping creation.")
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchEntity':
            print(f"IAM role {role_name} does not exist. Proceeding with creation.")
            response = iam_client.create_role(RoleName=role_name, AssumeRolePolicyDocument=json.dumps(trust_policy), )
            print(f"IAM role {role_name} created successfully.")
            return response
        else:
            print(f"An error occurred: {e}")
            raise e


def create_efs_role_with_policy(cluster_name, account_no, role_name,
                                service_account_name=get_efs_service_account_name(), namespace=NAMESPACE,
                                region=REGION):
    oidc_issuer_url = get_cluster_oidc_issuer_url(cluster_name)
    create_efs_driver_role(account_no, role_name, oidc_issuer_url, namespace, service_account_name)
    iam_client = boto3.client('iam', region_name=region)
    response = iam_client.attach_role_policy(PolicyArn='arn:aws:iam::aws:policy/service-role/AmazonEFSCSIDriverPolicy',
                                             RoleName=role_name, )
    return response


def create_efs_addon():
    # Execute the shell commands
    eks_client = boto3.client('eks', region_name=REGION)
    addon_name = 'aws-efs-csi-driver'
    cluster_name = get_cluster_name()
    service_account_role_arn = f'arn:aws:iam::{get_aws_account_id()}:role/{get_efs_role_name()}'
    try:
        # Check if the EFS addon already exists
        eks_client.describe_addon(clusterName=cluster_name, addonName=addon_name)
        print(f"EFS addon {addon_name} already exists in cluster {cluster_name}. Skipping creation.")
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print(f"EFS addon {addon_name} does not exist in cluster {cluster_name}. Proceeding with creation.")
            response = eks_client.create_addon(addonName=addon_name, clusterName=cluster_name,
                                               serviceAccountRoleArn=service_account_role_arn, )
            print(f"EFS addon {addon_name} created successfully in cluster {cluster_name}.")
            return response
        else:
            print(f"An error occurred: {e}")
            raise e


def create_efs_filesystem(name):
    efs_client = boto3.client('efs')

    try:
        # Describe file systems
        response = efs_client.describe_file_systems()

        # Filter the file systems by the tag name
        for fs in response['FileSystems']:
            tags = efs_client.describe_tags(FileSystemId=fs['FileSystemId'])['Tags']
            if any(tag['Key'] == 'Name' and tag['Value'] == name for tag in tags):
                filesystem_id = fs['FileSystemId']
                print(f"EFS File System {name} already exists with ID: {filesystem_id}. Skipping creation.")
                return filesystem_id

        print(f"EFS File System {name} does not exist. Proceeding with creation.")
    except ClientError as e:
        print(f"An error occurred while checking for EFS filesystem: {e}")
        raise e

    try:
        # Create the EFS filesystem if it does not exist
        response = efs_client.create_file_system(CreationToken=name, PerformanceMode='generalPurpose',
                                                 ThroughputMode='elastic', Encrypted=True)
        filesystem_id = response['FileSystemId']
        print(f"EFS File System Created with ID: {filesystem_id}")
        efs_client.create_tags(FileSystemId=filesystem_id, Tags=[{'Key': 'Name', 'Value': name}])
        return filesystem_id
    except ClientError as e:
        print(f"An error occurred while creating the EFS filesystem: {e}")
        raise e


def get_efs_filesystem_by_name(name: str):
    efs_client = boto3.client('efs')

    # Get all file systems
    response = efs_client.describe_file_systems()

    # Iterate over all file systems
    for filesystem in response['FileSystems']:
        # Get the tags for the current file system
        tags_response = efs_client.describe_tags(FileSystemId=filesystem['FileSystemId'])

        # Check if the 'Name' tag matches the desired name
        for tag in tags_response['Tags']:
            if tag['Key'] == 'Name' and tag['Value'] == name:
                return filesystem

    return None


def wait_for_efs_filesystem(filesystem_id):
    efs_client = boto3.client('efs')
    while True:
        response = efs_client.describe_file_systems(FileSystemId=filesystem_id)
        lifecycle_state = response['FileSystems'][0]['LifeCycleState']
        if lifecycle_state == 'available':
            print(f"EFS File System {filesystem_id} is now available.")
            break
        print(f"Waiting for EFS File System {filesystem_id} to become available. Current state: {lifecycle_state}")
        time.sleep(5)


def create_security_group(vpc_id, env: Optional[str] = None):
    ec2_client = boto3.client('ec2')
    group_name = get_efs_security_group_name(env=env)
    # Check if the security group already exists
    try:
        response = ec2_client.describe_security_groups(Filters=[{'Name': 'group-name', 'Values': [group_name]}])
        if response['SecurityGroups']:
            print(f"Security Group '{group_name}' already exists with ID: {response['SecurityGroups'][0]['GroupId']}")
            return response['SecurityGroups'][0]['GroupId']
    except ClientError as e:
        print(f"Error checking for existing security group: {e}")

    # Create the security group if it does not exist
    try:
        response = ec2_client.create_security_group(GroupName=group_name, Description='Security group for EFS',
                                                    VpcId=vpc_id)
        security_group_id = response['GroupId']
        print(f"Security Group Created with ID: {security_group_id}")
        return security_group_id
    except ClientError as e:
        print(f"Error creating security group: {e}")
        return None


def authorize_security_group_ingress(security_group_id, cidr_range):
    ec2_client = boto3.client('ec2')

    # Describe existing security group rules
    response = ec2_client.describe_security_groups(GroupIds=[security_group_id])
    security_group = response['SecurityGroups'][0]
    existing_permissions = security_group['IpPermissions']

    # Check if the rule already exists
    rule_exists = False
    for permission in existing_permissions:
        if (permission['IpProtocol'] == 'tcp' and permission['FromPort'] == 2049 and permission['ToPort'] == 2049):
            for ip_range in permission['IpRanges']:
                if ip_range['CidrIp'] == cidr_range:
                    rule_exists = True
                    break
        if rule_exists:
            break

    # Add the rule only if it does not exist
    if not rule_exists:
        ec2_client.authorize_security_group_ingress(GroupId=security_group_id, IpPermissions=[
            {'IpProtocol': 'tcp', 'FromPort': 2049, 'ToPort': 2049, 'IpRanges': [{'CidrIp': cidr_range}]}])
        print(f"Inbound rule for NFS traffic added to security group {security_group_id}")
    else:
        print(f"Inbound rule for NFS traffic already exists in security group {security_group_id}")


def get_az_from_subnet(subnet_id):
    ec2_client = boto3.client('ec2')
    response = ec2_client.describe_subnets(SubnetIds=[subnet_id])
    return response['Subnets'][0]['AvailabilityZone']


def create_efs_mount_targets(filesystem_id, subnets, security_group_id):
    efs_client = boto3.client('efs')

    # Get existing mount targets for the file system
    existing_mount_targets = efs_client.describe_mount_targets(FileSystemId=filesystem_id)['MountTargets']

    existing_azs = {get_az_from_subnet(mt['SubnetId']) for mt in existing_mount_targets}

    for subnet in subnets:
        az = get_az_from_subnet(subnet)
        if az not in existing_azs:
            efs_client.create_mount_target(FileSystemId=filesystem_id, SubnetId=subnet,
                                           SecurityGroups=[security_group_id])
            print(f"Mount Target Created in Subnet {subnet} (AZ: {az})")
            existing_azs.add(az)  # Add the AZ to the set to avoid duplicate creation
        else:
            print(f"Mount Target already exists in AZ {az} (Subnet {subnet})")

    return True


def configure_efs_for_the_cluster(env: Optional[str] = None):
    cluster_name = get_cluster_name()
    vpc_config = get_eks_cluster_vpc_config(cluster_name)
    vpc_id = vpc_config['vpcId']
    subnets = vpc_config['subnetIds']

    file_system_id = create_efs_filesystem(name=get_efs_name(cluster_name, env))
    wait_for_efs_filesystem(filesystem_id=file_system_id)
    cidr_range = get_vpc_cidr(vpc_id)

    security_group_id = create_security_group(vpc_id=vpc_id, env=env)
    authorize_security_group_ingress(security_group_id, cidr_range)
    create_efs_mount_targets(file_system_id, subnets, security_group_id)


def apply_storage_class(context_name: Optional[str] = None):
    # Load the Kubernetes configuration
    if not context_name:
        context_name = get_tensorkube_cluster_context_name()
        if not context_name:
            return None
    k8s_api_client = config.new_client_from_config(context=context_name)

    # Load the storage class YAML configuration
    with open(resource_filename('tensorkube', 'configurations/efs_configs/storage_class.yaml'), 'r') as f:
        storage_class_yaml = yaml.safe_load(f)

    # Get the storage class name from the YAML (assuming 'metadata' and 'name' fields exist)
    storage_class_name = storage_class_yaml['metadata']['name']

    # Create an instance of the StorageV1Api
    api_instance = client.StorageV1Api(k8s_api_client)

    # List existing storage classes
    existing_storage_classes = api_instance.list_storage_class().items

    # Check if the storage class already exists
    if any(sc.metadata.name == storage_class_name for sc in existing_storage_classes):
        click.echo(f"Storage class '{storage_class_name}' already exists")
    else:
        # Create the storage class
        api_instance.create_storage_class(body=storage_class_yaml)
        click.echo("Storage class created")


def configure_efs():
    create_efs_role_with_policy(cluster_name=get_cluster_name(), account_no=get_aws_account_id(),
                                role_name=get_efs_role_name())
    create_efs_addon()
    configure_efs_for_the_cluster()
    apply_storage_class()
    apply_efs_pv()
    apply_efs_pvc()


def apply_efs_pv(env: Optional[str] = None, context_name: Optional[str] = None):
    # Load the Kubernetes configuration
    if not context_name:
        context_name = get_tensorkube_cluster_context_name()
        if not context_name:
            return None
    k8s_api_client = config.new_client_from_config(context=context_name)

    # Load the PV YAML configuration
    with open(resource_filename('tensorkube', 'configurations/efs_configs/efs_pv.yaml'), 'r') as f:
        pv_yaml = yaml.safe_load(f)

    # Get filesystem ID
    filesystem = get_efs_filesystem_by_name(get_efs_name(cluster_name=get_cluster_name(), env=env))
    pv_yaml['spec']['csi']['volumeHandle'] = filesystem['FileSystemId']
    pv_yaml['metadata']['name'] = get_efs_pv_name(env=env)

    # Get the PV name from the YAML (assuming 'metadata' and 'name' fields exist)
    pv_name = pv_yaml['metadata']['name']

    # Create an instance of the CoreV1Api
    api_instance = client.CoreV1Api(k8s_api_client)

    # List existing persistent volumes
    existing_pvs = api_instance.list_persistent_volume().items

    # Check if the PV already exists
    if any(pv.metadata.name == pv_name for pv in existing_pvs):
        click.echo(f"Persistent volume '{pv_name}' already exists")
    else:
        # Create the persistent volume
        api_instance.create_persistent_volume(body=pv_yaml)
        click.echo("Persistent volume created")


def apply_efs_pvc(env: Optional[str] = None, context_name: Optional[str] = None):
    # Load the Kubernetes configuration
    if not context_name:
        context_name = get_tensorkube_cluster_context_name()
        if not context_name:
            return None
    k8s_api_client = config.new_client_from_config(context=context_name)

    # Load the PVC YAML configuration
    with open(resource_filename('tensorkube', 'configurations/efs_configs/efs_pvc.yaml'), 'r') as f:
        pvc_yaml = yaml.safe_load(f)

    pvc_yaml['metadata']['name'] = get_efs_pvc_name(env=env)
    env_namespace = env if env else DEFAULT_NAMESPACE

    # Get the PVC name from the YAML (assuming 'metadata' and 'name' fields exist)
    pvc_name = pvc_yaml['metadata']['name']

    # Create an instance of the CoreV1Api
    api_instance = client.CoreV1Api(k8s_api_client)

    # List existing persistent volume claims in the specified namespace
    existing_pvcs = api_instance.list_namespaced_persistent_volume_claim(namespace=env_namespace).items

    # Check if the PVC already exists
    if any(pvc.metadata.name == pvc_name for pvc in existing_pvcs):
        click.echo(f"Persistent volume claim '{pvc_name}' already exists")
    else:
        # Create the persistent volume claim
        api_instance.create_namespaced_persistent_volume_claim(namespace=env_namespace, body=pvc_yaml)
        click.echo("Persistent volume claim created")


def delete_efs_filesystem(name: str):
    efs_client = boto3.client('efs')
    filesystem = get_efs_filesystem_by_name(name)
    if filesystem:
        filesystem_id = filesystem['FileSystemId']

        # Delete mount targets
        mount_targets = efs_client.describe_mount_targets(FileSystemId=filesystem_id)['MountTargets']
        for mount_target in mount_targets:
            efs_client.delete_mount_target(MountTargetId=mount_target['MountTargetId'])
            print(f"Deleted mount target {mount_target['MountTargetId']}")

        # Wait for mount targets to be deleted
        while True:
            mount_targets = efs_client.describe_mount_targets(FileSystemId=filesystem_id)['MountTargets']
            if not mount_targets:
                break
            print("Waiting for mount targets to be deleted. Current mount target IDs:",
                  list(map(lambda mt: mt['MountTargetId'], mount_targets)))
            time.sleep(5)

        # Delete the EFS file system
        efs_client.delete_file_system(FileSystemId=filesystem_id)
        print(f"EFS File System {filesystem_id} deleted")
    else:
        print(f"EFS File System with name {name} not found")


import time
from botocore.exceptions import ClientError


def delete_efs_addon():
    eks_client = boto3.client('eks', region_name=REGION)
    addon_name = 'aws-efs-csi-driver'
    cluster_name = get_cluster_name()
    try:
        eks_client.delete_addon(clusterName=cluster_name, addonName=addon_name)
        print(f"Initiated deletion of EFS addon {addon_name} from cluster {cluster_name}.")

        # Wait for deletion to complete
        max_attempts = 20
        sleep_time = 15  # seconds
        attempts = 0
        while attempts < max_attempts:
            try:
                response = eks_client.describe_addon(clusterName=cluster_name, addonName=addon_name)
                if response['addon']['status'] == 'DELETED':
                    print(f"EFS addon {addon_name} deleted successfully from cluster {cluster_name}.")
                    break
            except ClientError as e:
                if e.response['Error']['Code'] == 'ResourceNotFoundException':
                    print(f"EFS addon {addon_name} is successfully deleted from cluster {cluster_name}.")
                    break
                else:
                    print(f"An error occurred while checking EFS addon deletion status: {e}")
            time.sleep(sleep_time)
            attempts += 1
        if attempts == max_attempts:
            print(f"Timeout waiting for EFS addon {addon_name} to be deleted from cluster {cluster_name}.")
    except ClientError as e:
        print(f"An error occurred while deleting EFS addon: {e}")
        raise e


def delete_security_group(security_group_name: str):
    security_group_id = get_security_group_id_by_name(security_group_name)
    if not security_group_id:
        return
    ec2_client = boto3.client('ec2')
    ec2_client.delete_security_group(GroupId=security_group_id)
    print(f"Security Group {security_group_id} deleted")


def delete_storage_class(storage_class_name, context_name: Optional[str] = None):
    # Load the Kubernetes configuration
    if not context_name:
        context_name = get_tensorkube_cluster_context_name()
        if not context_name:
            return None
    k8s_api_client = config.new_client_from_config(context=context_name)

    # Create an instance of the StorageV1Api
    api_instance = client.StorageV1Api(k8s_api_client)

    try:
        # Delete the storage class
        api_instance.delete_storage_class(name=storage_class_name)
        click.echo(f"Storage class '{storage_class_name}' deleted successfully.")
    except client.exceptions.ApiException as e:
        if e.status == 404:
            click.echo(f"Storage class '{storage_class_name}' not found.")
        else:
            click.echo(f"An error occurred: {e}")


def cleanup_filesystem_resources():
    delete_pvc_using_name_and_namespace("efs-pvc", DEFAULT_NAMESPACE)
    delete_pv_using_name("efs-pv")
    delete_storage_class(storage_class_name='efs-sc')
    delete_efs_addon()
    delete_efs_filesystem(f'{get_cluster_name()}-efs')
    delete_security_group(get_efs_security_group_name())
    delete_iam_role(get_efs_role_name())


def delete_efs_directory_for_deployment(sanitised_project_name: str, env: Optional[str] = None,
                            context_name: Optional[str] = None):
    if not context_name:
        context_name = get_tensorkube_cluster_context_name()
        if not context_name:
            return None
    k8s_api_client = config.new_client_from_config(context=context_name)

    cleanup_config_file_path = resource_filename('tensorkube', 'configurations/build_configs/efs_cleanup_pod.yaml')
    with open(cleanup_config_file_path) as f:
        cleanup_config = yaml.safe_load(f)
    cleanup_config['metadata']['name'] = 'cleanup-{}'.format(sanitised_project_name)
    namespace_to_use = env if env else DEFAULT_NAMESPACE  # Replace 'default' with your default namespace if needed
    cleanup_config['metadata']['namespace'] = namespace_to_use
    cleanup_config['spec']['ttlSecondsAfterFinished'] = 100

    for volume in cleanup_config['spec']['template']['spec']['volumes']:
        if volume['name'] == 'efs-pvc':
            volume['persistentVolumeClaim']['claimName'] = get_efs_claim_name(env_name=env)

    cleanup_config['spec']['template']['spec']['containers'][0]['command'] = ["/bin/sh", "-c",
                                                                              f"""rm -rf /mnt/efs/images/{sanitised_project_name}
        echo 'Deletion completed' """]

    utils.create_from_dict(k8s_api_client, cleanup_config)
    click.echo('Deployed a delete config job')
