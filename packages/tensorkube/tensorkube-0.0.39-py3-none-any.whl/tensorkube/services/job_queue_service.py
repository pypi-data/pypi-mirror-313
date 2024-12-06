import json
import os
import uuid
from typing import Optional, List

import boto3
import click
import yaml
from kubernetes import config, client
from kubernetes.client.rest import ApiException
from pkg_resources import resource_filename
from typing import Optional, List
from botocore.exceptions import ClientError

from tensorkube.constants import REGION, get_cluster_name
from tensorkube.helpers import sanitise_name, extract_workdir_from_dockerfile, extract_command_from_dockerfile
from tensorkube.services.aws_service import get_aws_account_id, get_bucket_name, get_credentials
from tensorkube.services.dynamodb_service import get_dynamodb_table_name
from tensorkube.services.eks_service import get_cluster_oidc_issuer_url, install_keda, delete_keda_from_cluster
from tensorkube.services.environment_service import delete_environment, create_new_environment
from tensorkube.services.filesystem_service import delete_efs_directory_for_deployment
from tensorkube.services.iam_service import create_sqs_access_policy, create_sqs_access_role, attach_role_policy, \
    get_role_name_for_prefix, create_dynamo_access_policy, delete_policy, detach_role_policy, delete_iam_role
from tensorkube.services.k8s_service import get_tensorkube_cluster_context_name, get_efs_claim_name, \
    list_keda_scaled_jobs, list_trigger_authentications, delete_trigger_authentication, create_service_account, \
    create_k8s_role, create_role_binding, create_aws_secret, is_existing_scaled_job
from tensorkube.services.knative_service import get_instance_family_from_gpu_type, get_supported_gpu_families
from tensorkube.services.s3_service import create_s3_bucket
from tensorkube.services.sqs_service import create_sqs_queue, queue_message, delete_sqs_queue



def create_cloud_resources_for_queued_job_support():
    cluster_name = get_cluster_name()
    oidc_issuer_url = get_cluster_oidc_issuer_url(cluster_name)

    sqs_policy_name = f"{cluster_name}-sqs-access-policy"
    role_name = f"{cluster_name}-sqs-access-role"
    policy = create_sqs_access_policy(sqs_policy_name)
    dyanmo_policy_name = f"{cluster_name}-dynamo-access-policy"
    create_dynamo_access_policy(dyanmo_policy_name)
    click.echo("Policy created")
    role = create_sqs_access_role(get_aws_account_id(), oidc_issuer_url, role_name, 'keda', 'keda-operator')
    click.echo("Role created")
    attach_role_policy(get_aws_account_id(), sqs_policy_name, role_name)
    attach_role_policy(get_aws_account_id(), dyanmo_policy_name, role_name)
    click.echo("Policy attached to role")

    # TODO!: on Nydus implementation, create new role and service account for combined access to SQS and DynamoDB to be used in ScaledJob
    eksctl_role = get_role_name_for_prefix(prefix=f"eksctl-{get_cluster_name()}-nodegroup-")
    attach_role_policy(account_no=get_aws_account_id(), policy_name=sqs_policy_name, role_name=eksctl_role)
    karpenter_role = get_role_name_for_prefix(prefix=f"KarpenterNodeRole-{get_cluster_name()}")
    attach_role_policy(account_no=get_aws_account_id(), policy_name=sqs_policy_name, role_name=karpenter_role)
    attach_role_policy(account_no=get_aws_account_id(), policy_name=dyanmo_policy_name, role_name=eksctl_role)
    attach_role_policy(account_no=get_aws_account_id(), policy_name=dyanmo_policy_name, role_name=karpenter_role)
    click.echo("SQS access policy attached to nodes")

    create_new_environment('keda')

    installed = install_keda(role['Role']['Arn'])
    if not installed:
        click.echo("Error installing Keda")
        return

    click.echo("Keda installed")
    create_trigger_authentication_for_aws_sqs(role['Role']['Arn'])
    click.echo("Trigger authentication created")
    # create train bucket for the keda environment
    bucket_name = get_bucket_name(env_name='keda', type='train')
    create_s3_bucket(bucket_name)
    create_aws_secret(get_credentials(),"keda")
    click.echo("S3 train bucket created for keda env")

    create_table_for_job_status(region=REGION)


def create_trigger_authentication_for_aws_sqs(sqs_access_iam_role_arn: str, context_name: Optional[str] = None):
    if not context_name:
        context_name = get_tensorkube_cluster_context_name()
        if not context_name:
            return None
    k8s_api_client = config.new_client_from_config(context=context_name)
    k8s_client = client.CustomObjectsApi(k8s_api_client)

    trigger_auth_file_path = resource_filename('tensorkube', 'configurations/build_configs/queue_trigger_auth.yaml')
    with open(trigger_auth_file_path, 'r') as f:
        trigger_auth_json = yaml.safe_load(f)
    trigger_auth_json['spec']['podIdentity']['roleArn'] = sqs_access_iam_role_arn

    k8s_client.create_namespaced_custom_object('keda.sh', 'v1alpha1', 'keda', 'triggerauthentications',
                                               trigger_auth_json)


def get_queue_name_for_job(job_name: str):
    sanitised_job_name = sanitise_name(job_name)
    return f"{get_cluster_name()}-{sanitised_job_name}-queue"



def get_job_queue_url_for_job(job_name: str):
    queue_name = get_queue_name_for_job(job_name)
    sqs = boto3.client('sqs', region_name=REGION)
    response = sqs.get_queue_url(QueueName=queue_name)
    return response['QueueUrl']


def is_existing_queued_job(job_name: str):
    return is_existing_scaled_job(job_name=job_name, namespace="keda")


def deploy_job(job_name: str, gpus: int, gpu_type: Optional[str], cpu: int, memory: int, max_scale: int,
               env: str , image_tag:str, update: bool = False, region: str = REGION, cwd: Optional[str] =None,
               sanitised_project_name: Optional[str] = None, secrets: List[str] = [],
               context_name: Optional[str] = None, job_type: Optional[str] = None):
    click.echo("Deploying job...")
    # Load kube config
    if not context_name:
        context_name = get_tensorkube_cluster_context_name()
        if not context_name:
            return None
    k8s_api_client = config.new_client_from_config(context=context_name)
    k8s_client = client.CustomObjectsApi(k8s_api_client)
    if job_type == 'axolotl':
        scaled_job_file_path = resource_filename('tensorkube',
                                           'configurations/build_configs/fine_tuning_scaled_job.yaml')
        with open(scaled_job_file_path, 'r') as f:
            scaled_job_yaml = f.read()

        scaled_job_yaml = scaled_job_yaml.replace('${IMAGE_TAG}', image_tag)
        scaled_job_yaml = scaled_job_yaml.replace('${GPUS}', str(gpus))
        scaled_job_yaml = scaled_job_yaml.replace('${GPU_TYPE}', gpu_type)
        scaled_job_json = yaml.safe_load(scaled_job_yaml)
        job_queue_url = create_sqs_queue(get_queue_name_for_job(job_name))

        bucket_name = get_bucket_name(env_name=env, type='train')
        scaled_job_json['metadata']['name'] = job_name
        scaled_job_json['spec']['triggers'][0]['metadata']['queueURL'] = job_queue_url
        scaled_job_json['spec']['jobTargetRef']['template']['spec']['containers'][0]['env'].extend([
            {'name': 'AWS_REGION', 'value': region}, {'name': 'QUEUE_URL', 'value': job_queue_url}, {'name': 'JOB_NAME', 'value': job_name}, {'name': 'LORA_ADAPTER_BUCKET', 'value': bucket_name}])
        scaled_job_json['spec']['triggers'][0]['metadata']['region'] = region
        scaled_job_json['spec']['maxReplicaCount'] = max_scale

        if secrets:
            scaled_job_json['spec']['jobTargetRef']['template']['spec']['volumes'].append({
                'name': 'secrets',
                'projected': {
                    'sources': [{
                        'secret': {
                            'name': secret_name
                        }
                    } for secret_name in secrets]
                }
            })

            scaled_job_json['spec']['jobTargetRef']['template']['spec']['containers'][0]['volumeMounts'].append({
                'name': 'secrets',
                'mountPath': '/mnt/secrets',
                'readOnly': True
            })
        scaled_job_json['spec']['jobTargetRef']['template']['spec']['nodeSelector'] = {
            'karpenter.k8s.aws/instance-family': get_instance_family_from_gpu_type(gpu_type),
        }
        scaled_job_json['spec']['jobTargetRef']['template']['spec']['initContainers'][0]['command'] = ["/bin/sh", "-c", f"""\
            export QUEUE_URL={job_queue_url}
            export TABLE_NAME={get_dynamodb_table_name()}
            export JOB_NAME={job_name}
            export MSG=$(aws sqs receive-message --queue-url $QUEUE_URL --max-number-of-messages 1 --query 'Messages[0]')
            if [ "$MSG" == "null" ]; then
              echo "No message in queue"
            else
              echo $MSG | jq -r '.Body' | jq -r '.job_id' > /mnt/shared/sqs_message_id.txt
              echo $MSG | jq -r '.Body' | jq -r '.job_payload' > /mnt/shared/sqs_message_payload.txt
              echo $MSG | jq -r '.ReceiptHandle' > /mnt/shared/receipt_handle.txt
              echo "Message received with job_id: $(cat /mnt/shared/sqs_message_id.txt)" 
              aws dynamodb put-item --table-name $TABLE_NAME --item '{{
                "job_name": {{"S": "'"$JOB_NAME"'"}},
                "job_id": {{"S": "'"$(cat /mnt/shared/sqs_message_id.txt)"'"}},
                "status": {{"S": "PROCESSING"}}
              }}'
            fi
            """]
        scaled_job_json['spec']['jobTargetRef']['template']['spec'][
            'serviceAccountName'] = get_job_sidecar_service_account_name()
        scaled_job_json['spec']['jobTargetRef']['template']['spec']['containers'][1]['env'] = [
            {'name': 'AWS_REGION', 'value': region}]
        scaled_job_json['spec']['jobTargetRef']['template']['spec']['containers'][1]['command'] = ["/bin/sh", "-c", f"""\
             export QUEUE_URL={job_queue_url}
             export TABLE_NAME={get_dynamodb_table_name()}
             export JOB_NAME={job_name}
             echo "Tracking job status"
             while true; do
                    status=$(kubectl get pod ${{HOSTNAME}} -n keda -o jsonpath='{{.status.containerStatuses[?(@.name=="sqs-job-1")].state.terminated}}')
                    if [ -n "$status" ]; then
                        echo "Main container finished."
                        aws sqs delete-message --queue-url $QUEUE_URL --receipt-handle $(cat /mnt/shared/receipt_handle.txt) --region $AWS_REGION
                        
                        exit_code=$(kubectl get pod ${{HOSTNAME}} -n keda -o jsonpath='{{.status.containerStatuses[?(@.name=="sqs-job-1")].state.terminated.exitCode}}')
                        if [ "$exit_code" -eq 0 ]; then
                          echo "Main container succeeded. Running post-completion command."
                          aws dynamodb put-item --table-name $TABLE_NAME --item '{{ "job_name": {{"S": "'"$JOB_NAME"'"}},
                                "job_id": {{"S": "'"$(cat /mnt/shared/sqs_message_id.txt)"'"}}, "status": {{"S": "SUCCESS"}} }}' --region $AWS_REGION
                        else
                          echo "Main container failed. Running post-error command."
                            aws dynamodb put-item --table-name $TABLE_NAME --item '{{ "job_name": {{"S": "'"$JOB_NAME"'"}},
                                "job_id": {{"S": "'"$(cat /mnt/shared/sqs_message_id.txt)"'"}}, "status": {{"S": "ERROR"}} }}' --region $AWS_REGION
                        fi
                        break
                      fi
                      sleep 5
                    done
            """]
        
    else:
        dockerfile_path = cwd + "/Dockerfile"
        workdir = extract_workdir_from_dockerfile(dockerfile_path)
        command = extract_command_from_dockerfile(dockerfile_path)

        scaled_job_file_path = resource_filename('tensorkube', 'configurations/build_configs/scaled_job.yaml')
        with open(scaled_job_file_path, 'r') as f:
            scaled_job_json = yaml.safe_load(f)

        job_queue_url = create_sqs_queue(get_queue_name_for_job(job_name))

        scaled_job_json['metadata']['name'] = job_name
        scaled_job_json['spec']['triggers'][0]['metadata']['queueURL'] = job_queue_url
        scaled_job_json['spec']['jobTargetRef']['template']['spec']['containers'][0]['env'] = [
            {'name': 'AWS_REGION', 'value': region}, {'name': 'QUEUE_URL', 'value': job_queue_url},
            {'name': 'JOB_NAME', 'value': job_name}]
        scaled_job_json['spec']['triggers'][0]['metadata']['region'] = region
        scaled_job_json['spec']['maxReplicaCount'] = max_scale
    
        scaled_job_json['spec']['jobTargetRef']['template']['spec']['initContainers'][0]['env'] = [
            {'name': 'AWS_REGION', 'value': region}]
        scaled_job_json['spec']['jobTargetRef']['template']['spec']['initContainers'][0]['command'] = ["/bin/sh", "-c", f"""\
            export QUEUE_URL={job_queue_url}
            export TABLE_NAME={get_dynamodb_table_name()}
            export JOB_NAME={job_name}
            export MSG=$(aws sqs receive-message --queue-url $QUEUE_URL --max-number-of-messages 1 --query 'Messages[0]')
            if [ "$MSG" == "null" ]; then
              echo "No message in queue"
            else
              echo $MSG | jq -r '.Body' | jq -r '.job_id' > /mnt/shared/sqs_message_id.txt
              echo $MSG | jq -r '.Body' | jq -r '.job_payload' > /mnt/shared/sqs_message_payload.txt
              echo $MSG | jq -r '.ReceiptHandle' > /mnt/shared/receipt_handle.txt
              echo "Message received with job_id: $(cat /mnt/shared/sqs_message_id.txt)" 
              aws dynamodb put-item --table-name $TABLE_NAME --item '{{
                "job_name": {{"S": "'"$JOB_NAME"'"}},
                "job_id": {{"S": "'"$(cat /mnt/shared/sqs_message_id.txt)"'"}},
                "status": {{"S": "PROCESSING"}}
              }}'
            fi
            """]
    
        scaled_job_json['spec']['jobTargetRef']['template']['spec'][
            'serviceAccountName'] = get_job_sidecar_service_account_name()
        scaled_job_json['spec']['jobTargetRef']['template']['spec']['containers'][1]['env'] = [
            {'name': 'AWS_REGION', 'value': region}]
        scaled_job_json['spec']['jobTargetRef']['template']['spec']['containers'][1]['command'] = ["/bin/sh", "-c", f"""\
             export QUEUE_URL={job_queue_url}
             export TABLE_NAME={get_dynamodb_table_name()}
             export JOB_NAME={job_name}
             echo "Tracking job status"
             while true; do
                    status=$(kubectl get pod ${{HOSTNAME}} -n keda -o jsonpath='{{.status.containerStatuses[?(@.name=="sqs-job-1")].state.terminated}}')
                    if [ -n "$status" ]; then
                        echo "Main container finished."
                        aws sqs delete-message --queue-url $QUEUE_URL --receipt-handle $(cat /mnt/shared/receipt_handle.txt) --region $AWS_REGION
                        
                        exit_code=$(kubectl get pod ${{HOSTNAME}} -n keda -o jsonpath='{{.status.containerStatuses[?(@.name=="sqs-job-1")].state.terminated.exitCode}}')
                        if [ "$exit_code" -eq 0 ]; then
                          echo "Main container succeeded. Running post-completion command."
                          aws dynamodb put-item --table-name $TABLE_NAME --item '{{ "job_name": {{"S": "'"$JOB_NAME"'"}},
                                "job_id": {{"S": "'"$(cat /mnt/shared/sqs_message_id.txt)"'"}}, "status": {{"S": "SUCCESS"}} }}' --region $AWS_REGION
                        else
                          echo "Main container failed. Running post-error command."
                            aws dynamodb put-item --table-name $TABLE_NAME --item '{{ "job_name": {{"S": "'"$JOB_NAME"'"}},
                                "job_id": {{"S": "'"$(cat /mnt/shared/sqs_message_id.txt)"'"}}, "status": {{"S": "ERROR"}} }}' --region $AWS_REGION
                        fi
                        break
                      fi
                      sleep 5
                    done
            """]

        for volume in scaled_job_json['spec']['jobTargetRef']['template']['spec']['volumes']:
            if volume['name'] == 'efs-storage':
                volume['persistentVolumeClaim']['claimName'] = get_efs_claim_name(env_name=env)
    
        if secrets:
            scaled_job_json['spec']['jobTargetRef']['template']['spec']['volumes'].append({'name': 'secrets',
                'projected': {'sources': [{'secret': {'name': secret_name}} for secret_name in secrets]}})
    
            scaled_job_json['spec']['jobTargetRef']['template']['spec']['containers'][0]['volumeMounts'].append(
                {'name': 'secrets', 'mountPath': '/mnt/secrets', 'readOnly': True})
    
        scaled_job_json['spec']['jobTargetRef']['template']['spec']['containers'][0]['resources'] = {'requests': {},
                                                                                                     'limits': {}}
        if gpus > 0:
            if memory > 2000:
                scaled_job_json['spec']['template']['spec']['containers'][0]['resources']['requests'][
                    'memory'] = f'{str(int(memory))}M'
            if cpu > 2000:
                scaled_job_json['spec']['template']['spec']['containers'][0]['resources']['requests'][
                    'cpu'] = f'{str(int(cpu))}m'
            config_nvidia_ctk_commands = """sudo nvidia-ctk cdi generate --output=/etc/cdi/nvidia.yaml
                           nvidia-ctk cdi list
                        """
            podman_gpu_tags = "--gpus all --env NVIDIA_VISIBLE_DEVICES=all --env NVIDIA_DRIVER_CAPABILITIES=compute,utility"
    
            scaled_job_json['spec']['jobTargetRef']['template']['spec']['containers'][0][
                'image'] = "tensorfuse/podman-nvidia:v1"
    
            scaled_job_json['spec']['jobTargetRef']['template']['spec']['containers'][0]['resources']['requests'][
                'nvidia.com/gpu'] = gpus
            scaled_job_json['spec']['jobTargetRef']['template']['spec']['containers'][0]['resources']['limits'][
                'nvidia.com/gpu'] = gpus
    
            scaled_job_json['spec']['jobTargetRef']['template']['spec']['nodeSelector'] = {
                'karpenter.k8s.aws/instance-family': get_instance_family_from_gpu_type(gpu_type)}
        else:
            config_nvidia_ctk_commands = ""
            podman_gpu_tags = ""

            scaled_job_json['spec']['jobTargetRef']['template']['spec']['containers'][0][
                'image'] = "quay.io/podman/stable"
    
            scaled_job_json['spec']['jobTargetRef']['template']['spec']['containers'][0]['resources']['requests'][
                'cpu'] = f'{str(int(cpu))}m'
            scaled_job_json['spec']['jobTargetRef']['template']['spec']['containers'][0]['resources']['requests'][
                'memory'] = f'{str(int(memory))}M'
            scaled_job_json['spec']['jobTargetRef']['template']['spec']['containers'][0]['resources']['limits'][
                'cpu'] = f'{str(int(cpu))}m'
            scaled_job_json['spec']['jobTargetRef']['template']['spec']['containers'][0]['resources']['limits'][
                'memory'] = f'{str(int(memory))}M'

            scaled_job_json['spec']['jobTargetRef']['template']['spec']['affinity'] = {
                "nodeAffinity": {
                    "requiredDuringSchedulingIgnoredDuringExecution": {
                    "nodeSelectorTerms": [ {
                        "matchExpressions": [ {
                            "key": "karpenter.k8s.aws/instance-family",
                            "operator": "NotIn",
                            "values": get_supported_gpu_families()
                        } ]
                    } ]
            }}}

        if workdir:
            final_command = f"cd {workdir} && {command}"
        else:
            final_command = command

        if secrets:
            secrets_to_env_vars_command = """\
    folder_path="/mnt/secrets"

    # Initialize an empty string to hold the environment variables
    env_vars=""

    # Loop through each file in the folder
    for file in "$folder_path"/*; do
    if [[ -f $file ]]; then
        # Get the filename without the path
        filename=$(basename "$file")

        # Get the contents of the file
        contents=$(<"$file")

        # Escape the contents to handle any special characters or spaces
        escaped_contents=$(printf '%q' "$contents")

        # Append to the env_vars string in the format --env filename=contents
        env_vars="$env_vars --env $filename=$escaped_contents"
    fi
    done"""
        else:
            secrets_to_env_vars_command = "env_vars=''"

        scaled_job_json['spec']['jobTargetRef']['template']['spec']['containers'][0]['command'] = [
            "/bin/sh", "-c",f"""{config_nvidia_ctk_commands}
    {secrets_to_env_vars_command}
            sed -i 's|mount_program = "/usr/bin/fuse-overlayfs"|mount_program = ""|' /etc/containers/storage.conf
            sudo podman run --name mycontainer $env_vars  --env QUEUE_URL={job_queue_url} --env AWS_REGION={region} --env JOB_NAME={job_name} \
            -v /mnt/shared:/mnt/shared \
             {podman_gpu_tags} --network=host \
             --rootfs /mnt/efs/images/{sanitised_project_name}/{image_tag}/rootfs:O sh -c "{final_command}" """]

    if update:
        try:
            group = "keda.sh"
            version = "v1alpha1"
            namespace = "keda"
            plural = "scaledjobs"
            existing_job = k8s_client.get_namespaced_custom_object(group, version, namespace, plural, job_name)
            scaled_job_json['metadata']['resourceVersion'] = existing_job['metadata']['resourceVersion']
            k8s_client.replace_namespaced_custom_object(group, version, namespace, plural, job_name, scaled_job_json)
            click.echo("Job updated successfully.")
        except Exception as e:
            print(f"Error while updating job: {e}")
    else:
        try:
            group = "keda.sh"
            version = "v1alpha1"
            namespace = "keda"
            plural = "scaledjobs"
            k8s_client.create_namespaced_custom_object(group, version, namespace, plural, scaled_job_json)
            click.echo("Job deployed successfully.")
            click.echo(f"Run the job by running: tensorkube job queue --job-name {job_name} --job-id <job_id> --payload <payload>")
        except Exception as e:
            print(f"Error while deploying job: {e}")

def queue_job(job_name: str, job_id: str, job_payload: str, region: str = REGION):
    dynamodb = boto3.resource('dynamodb', region_name=region)
    table_name = f"{get_cluster_name()}-job-status"
    table = dynamodb.Table(table_name)

    # Check if the job already exists
    try:
        response = table.get_item(Key={'job_name': job_name, 'job_id': job_id})
        if 'Item' in response:
            raise Exception(f"Job {job_name} with ID {job_id} already exists. Skipping queue.")
    except Exception as e:
        print(f"Error checking job existence: {e}")
        raise e
    queur_url = get_job_queue_url_for_job(job_name)
    msg = {"job_id": job_id, "job_payload": job_payload}
    msg_str = json.dumps(msg)
    queue_message(queur_url, msg_str, region=REGION)
    set_job_status(job_name, job_id, status="QUEUED")


def delete_job(job_name: str, context_name: Optional[str] = None):
    if not context_name:
        context_name = get_tensorkube_cluster_context_name()
        if not context_name:
            return None

    k8s_api_client = config.new_client_from_config(context=context_name)
    k8s_client = client.CustomObjectsApi(k8s_api_client)

    try:
        group = "keda.sh"
        version = "v1alpha1"
        namespace = "keda"
        plural = "scaledjobs"
        k8s_client.delete_namespaced_custom_object(group, version, namespace, plural, job_name)
        click.echo(f"Job {job_name} deleted successfully.")
    except Exception as e:
        print(f"Error while deleting job: {e}")


def delete_all_job_resources(job_name: str):
    delete_job(job_name=job_name)
    queue_name = get_queue_name_for_job(job_name)
    delete_sqs_queue(queue_name)
    delete_job_in_dynamo(job_name)
    delete_efs_directory_for_deployment(sanitise_name(job_name), 'keda')


def delete_job_in_dynamo(job_name: str):
    dynamodb = boto3.resource('dynamodb', region_name=REGION)
    table = dynamodb.Table(get_dynamodb_table_name())
     # Query items with the specific partition key
    response = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key("job_name").eq(job_name)
    )
    #TODO: Handle pagination
    items = response.get('Items', [])
    with table.batch_writer() as batch:
        for item in items:
            batch.delete_item(
                Key={"job_name": item["job_name"], "job_id": item["job_id"]}
            )
    
    click.echo(f"Job {job_name} deleted from DynamoDB.")

def delete_dynamo_table():
    dynamodb = boto3.resource('dynamodb', region_name=REGION)
    table_name = get_dynamodb_table_name()
    try:
        table = dynamodb.Table(table_name)
        table.delete()
        print(f"Table {table_name} deleted successfully.")
    except Exception as e:
        print(f"Error deleting table: {e}")


def teardown_job_queue_support():
    jobs = list_keda_scaled_jobs()
    for job in jobs['items']:
        job_name = job['metadata']['name']
        delete_all_job_resources(job_name)

    trigger_auths = list_trigger_authentications()
    for trigger_auth in trigger_auths['items']:
        trigger_auth_name = trigger_auth['metadata']['name']
        delete_trigger_authentication(trigger_auth_name)
    delete_dynamo_table()
    cluster_name = get_cluster_name()
    sqs_policy_name = f"{cluster_name}-sqs-access-policy"
    sqs_role_name = f"{cluster_name}-sqs-access-role"
    dynamo_policy_name = f"{cluster_name}-dynamo-access-policy"

    eksctl_role = get_role_name_for_prefix(prefix=f"eksctl-{get_cluster_name()}-nodegroup-")
    karpenter_role = get_role_name_for_prefix(prefix=f"KarpenterNodeRole-{get_cluster_name()}")

    detach_role_policy(account_no=get_aws_account_id(), policy_name=sqs_policy_name, role_name=eksctl_role)
    detach_role_policy(account_no=get_aws_account_id(), policy_name=sqs_policy_name, role_name=karpenter_role)
    detach_role_policy(account_no=get_aws_account_id(), policy_name=dynamo_policy_name, role_name=eksctl_role)
    detach_role_policy(account_no=get_aws_account_id(), policy_name=dynamo_policy_name, role_name=karpenter_role)

    detach_role_policy(account_no=get_aws_account_id(), policy_name=sqs_policy_name, role_name=sqs_role_name)
    delete_policy(account_no=get_aws_account_id(), policy_name=sqs_policy_name)
    delete_iam_role(role_name=sqs_role_name)

    delete_policy(account_no=get_aws_account_id(), policy_name=dynamo_policy_name)

    delete_keda_from_cluster()
    delete_environment('keda')


# EXPOSE
def get_queued_message():
    payload_file_path = "/mnt/shared/sqs_message_payload.txt"
    if os.path.exists(payload_file_path):
        with open(payload_file_path, 'r') as file:
            return file.read()
    else:
        raise Exception("Payload file not found.")


def delete_queued_message(receipt_handle: str):
    sqs = boto3.client('sqs', region_name=REGION)
    queue_url = os.getenv('QUEUE_URL', None)
    if not queue_url:
        raise Exception("QUEUE_URL not set in environment variables.")

    response = sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
    return response


def create_table_for_job_status(region: str = REGION):
    table_name = get_dynamodb_table_name()
    dynamodb = boto3.resource('dynamodb', region_name=region)
    try:
        # Create the DynamoDB table
        table = dynamodb.create_table(TableName=table_name,
            KeySchema=[{'AttributeName': 'job_name', 'KeyType': 'HASH'  # Partition key
            }, {'AttributeName': 'job_id', 'KeyType': 'RANGE'  # Sort key
            }], AttributeDefinitions=[{'AttributeName': 'job_name', 'AttributeType': 'S'},
                {'AttributeName': 'job_id', 'AttributeType': 'S'}], BillingMode='PAY_PER_REQUEST'
            # Set BillingMode to On-Demand
        )

        # Wait until the table exists
        table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
        print(f"Table {table_name} created successfully.")

    except Exception as e:
        print(f"Error creating table: {e}")


# EXPOSE
def set_job_status(job_name: str, job_id: str, status: str):
    dynamodb = boto3.resource('dynamodb', region_name=REGION)
    table = dynamodb.Table(get_dynamodb_table_name())
    response = table.put_item(Item={'job_name': job_name, 'job_id': job_id, 'status': status})
    return response

#EXPOSE
def get_job_status(job_name: str, job_id: str):
    dynamodb = boto3.resource('dynamodb', region_name=REGION)
    table = dynamodb.Table(get_dynamodb_table_name())
    response = table.get_item(Key={'job_name': job_name, 'job_id': job_id})
    return response['Item']['status'] if 'Item' in response else None


def get_job_sidecar_service_account_name(namespace: Optional[str] = None):
    if not namespace:
        namespace = "keda"
    return f"job-queue-sidecar-{namespace}-sa"


def create_sa_role_rb_for_job_sidecar(namespace: Optional[str] = None):
    if not namespace:
        namespace = "keda"
    sa_name = get_job_sidecar_service_account_name(namespace)
    role_name = f"job-queue-sidecar-{namespace}-role"
    rb_name = f"job-queue-sidecar-{namespace}-rb"

    pod_tracking_rules = [{"apiGroups": [""], "resources": ["pods"], "verbs": ["get", "list"]}]

    create_service_account(name=sa_name, namespace=namespace)
    click.echo("Service Account created")
    create_k8s_role(role_name=role_name, rules=pod_tracking_rules, namespace=namespace)
    click.echo("Role created")
    create_role_binding(rb_name=rb_name, role_name=role_name, sa_name=sa_name, rb_namespace=namespace,
                        sa_namespace=namespace)
    click.echo("Role Binding created")
