import json

import boto3
from botocore.exceptions import ClientError
from pkg_resources import resource_filename
from typing import Dict

from tensorkube.constants import REGION, get_cluster_name
from tensorkube.services.aws_service import get_aws_account_id
import yaml

def create_iam_policy(policy_name: str, policy_document: Dict, region: str = REGION):
    iam = boto3.client('iam', region_name=region)
    sts = boto3.client('sts')
    try:
        # Check if the IAM policy already exists
        account_id = sts.get_caller_identity()['Account']
        policy_arn = f"arn:aws:iam::{account_id}:policy/{policy_name}"
        response = iam.get_policy(PolicyArn=policy_arn)
        print(f"IAM policy {policy_name} already exists. Skipping creation.")
        return response
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchEntity':
            print(f"IAM policy {policy_name} does not exist. Proceeding with creation.")
            response = iam.create_policy(PolicyName=policy_name, PolicyDocument=json.dumps(policy_document), )
            print(f"IAM policy {policy_name} created successfully.")
            return response
        else:
            print(f"An error occurred: {e}")
            raise e


def create_mountpoint_iam_policy(policy_name, bucket_name, region=REGION):
    policy_file_path = resource_filename('tensorkube', 'configurations/aws_configs/mountpoint_policy.json')
    with open(policy_file_path, 'r') as f:
        policy = json.load(f)
    for statement in policy['Statement']:
        statement['Resource'] = [r.replace('USER_BUCKET', bucket_name) for r in statement['Resource']]

    return create_iam_policy(policy_name, policy, region)


def create_sqs_access_policy(policy_name, region=REGION):
    policy_file_path = resource_filename('tensorkube', 'configurations/aws_configs/sqs_access_policy.json')
    with open(policy_file_path, 'r') as f:
        policy = json.load(f)
    for statement in policy['Statement']:
        statement['Resource'] = f"arn:aws:sqs:{region}:{get_aws_account_id()}:{get_cluster_name()}-*"
    return create_iam_policy(policy_name, policy, region)

def create_dynamo_access_policy(policy_name, region=REGION):
    policy_file_path = resource_filename('tensorkube', 'configurations/aws_configs/dynamo_access_policy.json')
    with open(policy_file_path, 'r') as f:
        policy = json.load(f)
    for statement in policy['Statement']:
        resource = statement['Resource']
        resource = resource.replace('REGION', region)
        resource = resource.replace('ACCOUNT_NO', get_aws_account_id())
        resource = resource.replace('TABLE_NAME', f"{get_cluster_name()}-*")
        statement['Resource'] = resource
    return create_iam_policy(policy_name, policy, region)



def create_iam_role_with_service_account_cluster_access(account_no: str, oidc_issuer_url: str, role_name: str,
                                                        service_account_name: str, namespace: str, region: str=REGION):
    oidc_issuer = oidc_issuer_url[8:]
    region = oidc_issuer.split('.')[2]
    trust_policy_file_path = resource_filename('tensorkube',
                                               'configurations/aws_configs/iam_role_cluster_access_trust_policy.json')
    with open(trust_policy_file_path, 'r') as f:
        trust_policy = json.load(f)
    trust_policy['Statement'][0]['Principal']['Federated'] = 'arn:aws:iam::{}:oidc-provider/{}'.format(account_no,
                                                                                                       oidc_issuer)
    trust_policy['Statement'][0]['Condition']['StringEquals'] = {
        "{}:sub".format(oidc_issuer): "system:serviceaccount:{}:{}".format(namespace, service_account_name),
        "{}:aud".format(oidc_issuer): "sts.amazonaws.com"}

    iam = boto3.client('iam', region_name=region)

    try:
        # Check if the IAM role already exists
        response = iam.get_role(RoleName=role_name)
        print(f"IAM role {role_name} already exists. Skipping creation.")
        return response
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchEntity':
            print(f"IAM role {role_name} does not exist. Proceeding with creation.")
            response = iam.create_role(RoleName=role_name, AssumeRolePolicyDocument=json.dumps(trust_policy), )
            print(f"IAM role {role_name} created successfully.")
            return response
        else:
            print(f"An error occurred: {e}")
            raise e


def create_s3_csi_driver_role(account_no: str, role_name: str, oidc_issuer_url: str, namespace: str,
                              service_account_name: str):
    create_iam_role_with_service_account_cluster_access(account_no, oidc_issuer_url, role_name, service_account_name,
                                                        namespace)


def create_sqs_access_role(account_no: str, oidc_issuer_url: str, role_name: str, namespace: str,
                           service_account_name: str):
    return create_iam_role_with_service_account_cluster_access(account_no, oidc_issuer_url, role_name, service_account_name,
                                                        namespace)


def attach_role_policy(account_no, policy_name, role_name, region=REGION):
    client = boto3.client('iam', region_name=region)
    response = client.attach_role_policy(PolicyArn='arn:aws:iam::{}:policy/{}'.format(account_no, policy_name),
                                         RoleName=role_name, )
    return response


def detach_role_policy(account_no, role_name, policy_name, region=REGION):
    client = boto3.client('iam', region_name=region)
    response = client.detach_role_policy(PolicyArn='arn:aws:iam::{}:policy/{}'.format(account_no, policy_name),
                                         RoleName=role_name, )
    return response


def delete_role(role_name, region=REGION):
    client = boto3.client('iam', region_name=region)
    response = client.delete_role(RoleName=role_name)
    return response


def delete_policy(account_no, policy_name, region=REGION):
    client = boto3.client('iam', region_name=region)
    response = client.delete_policy(PolicyArn='arn:aws:iam::{}:policy/{}'.format(account_no, policy_name))
    return response


def delete_iam_role(role_name):
    iam_client = boto3.client('iam')
    attached_policies = iam_client.list_attached_role_policies(RoleName=role_name)['AttachedPolicies']

    # Detach policies
    for policy in attached_policies:
        iam_client.detach_role_policy(RoleName=role_name, PolicyArn=policy['PolicyArn'])
        print(f"Detached policy {policy['PolicyArn']} from role {role_name}")

    # Delete the role
    iam_client.delete_role(RoleName=role_name)
    print(f"IAM Role {role_name} deleted")


def get_role_name_for_prefix(prefix: str):
    iam = boto3.client('iam')
    roles = []
    response = iam.list_roles()
    
    # Collect all roles, handling pagination
    while True:
        roles.extend(response['Roles'])
        if response.get('IsTruncated'):  # If there are more roles
            response = iam.list_roles(Marker=response['Marker'])
        else:
            break
    
    for role in roles:
        if role['RoleName'].startswith(prefix):
            return role['RoleName']
    return None

def create_iam_user(user_name, region=REGION):
    iam = boto3.client('iam', region_name=region)
    try:
        response = iam.create_user(UserName=user_name)
        print(f"IAM User '{user_name}' created successfully.")
        return response['User']
    except iam.exceptions.EntityAlreadyExistsException:
        print(f"IAM User '{user_name}' already exists.")
        return iam.get_user(UserName=user_name)['User']

def create_eks_access_policy(policy_name, region=REGION):
    policy_file_path = resource_filename('tensorkube', 'configurations/aws_configs/eks_access_policy.json')
    with open(policy_file_path, 'r') as f:
        policy = json.load(f)
    statements= []
    for statement in policy['Statement']:
        resource = statement['Resource'] 
        resource = resource.replace('CLUSTER_NAME', get_cluster_name())
        resource =resource.replace('REGION', region)
        resource = resource.replace('ACCOUNT_NO', get_aws_account_id())
        statement['Resource'] = resource
        statements.append(statement)
    policy['Statement'] = statements
    return create_iam_policy(policy_name, policy, region)


def create_user_sqs_access_policy(policy_name, region=REGION):
    policy_file_path = resource_filename('tensorkube', 'configurations/aws_configs/user_sqs_access_policy.json')
    with open(policy_file_path, 'r') as f:
        policy = json.load(f)
    for statement in policy['Statement']:
        statement['Resource'] = f"arn:aws:sqs:{region}:{get_aws_account_id()}:{get_cluster_name()}-*"
    return create_iam_policy(policy_name, policy, region)

def create_user_s3_access_policy(policy_name, region=REGION):
    policy_file_path = resource_filename('tensorkube', 'configurations/aws_configs/user_s3_access_policy.json')
    with open(policy_file_path, 'r') as f:
        policy = json.load(f)
    return create_iam_policy(policy_name, policy, region)

def create_user_dynamo_access_policy(policy_name, region=REGION):
    policy_file_path = resource_filename('tensorkube', 'configurations/aws_configs/user_dynamo_access_policy.json')
    with open(policy_file_path, 'r') as f:
        policy = json.load(f)
    for statement in policy['Statement']:
        statement['Resource'] = f"arn:aws:dynamodb:{region}:{get_aws_account_id()}:table/{get_cluster_name()}-*"
    return create_iam_policy(policy_name, policy, region)



def attach_policy_to_user(policy_arn, user_name, region=REGION):
    iam = boto3.client('iam', region_name=region)
    iam.attach_user_policy(UserName=user_name, PolicyArn=policy_arn)
    print(f"Policy '{policy_arn}' attached to user '{user_name}'.")


def create_access_key(user_name, region=REGION):
    iam = boto3.client('iam', region_name=region)
    response = iam.create_access_key(UserName=user_name)
    access_key = response['AccessKey']
    return access_key['AccessKeyId'], access_key['SecretAccessKey']




