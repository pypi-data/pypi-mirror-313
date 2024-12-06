import pprint
import threading
import time
from typing import Tuple

import botocore.exceptions
import click
from pkg_resources import resource_filename

from tensorkube.services.aws_service import get_cloudformation_client, get_ec2_client, get_iam_client
from tensorkube.constants import get_cluster_name


def create_cloudformation_stack()-> Tuple[bool, bool]:
    cloudformation_client = get_cloudformation_client()

    # stack name
    cluster_name = get_cluster_name()
    parameters = [{"ParameterKey": "ClusterName", 'ParameterValue': cluster_name}]

    file_name = resource_filename('tensorkube', 'configurations/karpenter_cloudformation.yaml')

    try:
        stack = cloudformation_client.describe_stacks(StackName=cluster_name)
        if stack['Stacks'][0]['StackStatus'] == 'CREATE_COMPLETE':
            click.echo(f"Stack {cluster_name} already exists. Skipping stack creation")
            creation_queued = False
            in_created_state = True
            return creation_queued, in_created_state
        elif stack['Stacks'][0]['StackStatus'] == 'CREATE_IN_PROGRESS':
            click.echo(f"Stack {cluster_name} already exists and is in creation state. Please wait for "
                       f"creation to complete.")
            creation_queued = True
            in_created_state = False
            return creation_queued, in_created_state
        elif stack['Stacks'][0]['StackStatus'] == 'ROLLBACK_COMPLETE':
            click.echo(f"Stack {cluster_name} already exists but is in rollback state. Please delete the stack "
                       f"and recreate it.")
            creation_queued = False
            in_created_state = False
            return creation_queued, in_created_state
        elif stack['Stacks'][0]['StackStatus'] == 'DELETE_COMPLETE':
            # use the configurations/karpenter_cloudformation.yaml in the library
            with open(file_name) as file:
                template = file.read()
            response = cloudformation_client.create_stack(StackName=cluster_name, TemplateBody=template, Parameters=parameters,
                                                          Capabilities=["CAPABILITY_NAMED_IAM"])
            creation_queued = True
            in_created_state = False
            return creation_queued, in_created_state
        else:
            click.echo(f"Stack {cluster_name} already exists but not in created state. Either wait for "
                       f"creation to complete or delete stack to recreate it.")
            creation_queued = False
            in_created_state = False
            return creation_queued, in_created_state
    except botocore.exceptions.ClientError as e:
        if 'does not exist' in str(e):
            # use the configurations/karpenter_cloudformation.yaml in the library
            with open(file_name) as file:
                template = file.read()
            response = cloudformation_client.create_stack(StackName=cluster_name, TemplateBody=template, Parameters=parameters,
                                                          Capabilities=["CAPABILITY_NAMED_IAM"])
            creation_queued = True
            in_created_state = False
            return creation_queued, in_created_state
        else:
            click.echo(e)
            raise Exception('Unable to create cloudformation cluster')


def delete_role_and_attached_policies(iam, role_name):
    # List all attached policies
    attached_policies = iam.list_attached_role_policies(RoleName=role_name)['AttachedPolicies']

    # Detach each policy
    for policy in attached_policies:
        iam.detach_role_policy(RoleName=role_name, PolicyArn=policy['PolicyArn'])
        if get_cluster_name() in policy['PolicyName']:
            # Delete the policy
            iam.delete_policy(PolicyArn=policy['PolicyArn'])

    # Delete the role
    iam.delete_role(RoleName=role_name)


def delete_cloudformation_stack(stack_name):
    cloudformation_client = get_cloudformation_client()

    try:
        cloudformation_client.describe_stacks(StackName=stack_name)
    except botocore.exceptions.ClientError as e:
        if 'does not exist' in str(e):
            print(f'Stack {stack_name} does not exist.')
            return
        else:
            raise
    iam = get_iam_client()

    role_name = f'KarpenterNodeRole-{get_cluster_name()}'

    # List all instance profiles
    instance_profiles = iam.list_instance_profiles()['InstanceProfiles']

    # For each instance profile
    for profile in instance_profiles:
        # Check if the role is associated with the instance profile
        for role in profile['Roles']:
            if role['RoleName'] == role_name:
                # Remove the role from the instance profile
                iam.remove_role_from_instance_profile(InstanceProfileName=profile['InstanceProfileName'],
                    RoleName=role_name)

                # Delete the instance profile
                iam.delete_instance_profile(InstanceProfileName=profile['InstanceProfileName'])

    # Delete the role
    delete_role_and_attached_policies(iam, role_name)

    response = cloudformation_client.delete_stack(StackName=stack_name)
    # Create a waiter to wait for the stack to be deleted
    waiter = cloudformation_client.get_waiter('stack_delete_complete')

    # Start streaming the stack events in a separate thread
    stream_stack_events(stack_name)

    # Wait for the stack to be deleted
    waiter.wait(StackName=stack_name, WaiterConfig={'MaxAttempts': 30})
    return response


def delete_launch_templates():
    ec2_client = get_ec2_client()
    cluster_name = get_cluster_name()
    # Describe the launch templates
    response = ec2_client.describe_launch_templates(
        Filters=[{'Name': 'tag:karpenter.k8s.aws/cluster', 'Values': [cluster_name]}])
    launch_template_names = [lt['LaunchTemplateName'] for lt in response['LaunchTemplates']]

    # Delete each launch template
    for name in launch_template_names:
        ec2_client.delete_launch_template(LaunchTemplateName=name)


def stream_stack_events(stack_name):
    seen_events = set()
    cf_client = get_cloudformation_client()
    while True:
        try:
            events = cf_client.describe_stack_events(StackName=stack_name)['StackEvents']
            for event in reversed(events):
                event_id = event['EventId']
                if event_id not in seen_events:
                    seen_events.add(event_id)
                    click.echo(
                        f"{event['Timestamp']} {event['ResourceStatus']} {event['ResourceType']} {event['LogicalResourceId']} {event.get('ResourceStatusReason', '')}")
            # Check if stack creation is complete
            stack_status = cf_client.describe_stacks(StackName=stack_name)['Stacks'][0]['StackStatus']
            if stack_status.endswith('_COMPLETE') or stack_status.endswith('_FAILED'):
                break
            time.sleep(5)
        except Exception as e:
            if stack_name in str(e) and 'does not exist' in str(e):
                break


def cloudformation():
    """Create a cloudformation stack."""
    click.echo("Creating cloudformation stack...")
    # create_cloudformation_stack()
    creation_queued, in_created_state = create_cloudformation_stack()
    if creation_queued:
        stream_stack_events(get_cluster_name())
    click.echo("Cloudformation stack created.")
