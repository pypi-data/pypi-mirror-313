import click
import boto3
import json
from pkg_resources import resource_filename
from tensorkube.constants import REGION, get_cluster_name


def get_or_create_ecr_repository(sanitised_project_name:str):
    ecr = boto3.client('ecr')
    repository_name = f"{get_cluster_name()}-{sanitised_project_name}"

    try:
        response = ecr.create_repository(
            repositoryName=repository_name
        )
        #TODO! verify if this works. deletion takes upto 24 hours.
        ecr_repo_lifecycle_policy_config_file_path = resource_filename('tensorkube', 
                                                                       'configurations/aws_configs/ecr_repo_lifecycle_policy.json')
        with open(ecr_repo_lifecycle_policy_config_file_path, 'r') as f:
            ecr_repo_lifecycle_policy = json.dumps(json.load(f))
        ecr.put_lifecycle_policy(
            repositoryName=repository_name,
            lifecyclePolicyText=ecr_repo_lifecycle_policy
        )
        return response['repository']['repositoryUri']
    except ecr.exceptions.RepositoryAlreadyExistsException:
        click.echo(f"Repository '{repository_name}' already exists.")
        response = ecr.describe_repositories(repositoryNames=[repository_name])
        return response['repositories'][0]['repositoryUri']


def list_all_repositories(region: str=REGION):
    #TODO! pagination
    #NOTE: right now only 100 repositories are returned.
    ecr = boto3.client('ecr', region_name=region)
    response = ecr.describe_repositories()
    return response['repositories']


def delete_ecr_repository(repository_name:str, region:str=REGION):
    ecr = boto3.client('ecr', region_name=region)
    response = ecr.delete_repository(
        repositoryName=repository_name,
        force=True
    )
    return response


def delete_all_tensorkube_ecr_repositories():
    repositories = list_all_repositories()
    for repo in repositories:
        if get_cluster_name() in repo['repositoryName']:
            click.echo(f"Deleting repository '{repo['repositoryName']}'...")
            delete_ecr_repository(repo['repositoryName'])
