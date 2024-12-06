import yaml
import click
import time
import os
import uuid

from kubernetes import client
from pkg_resources import resource_filename
from tensorkube.services.k8s_service import apply_k8s_buildkit_config, \
    find_and_delete_old_job, check_pod_status, start_streaming_pod, start_streaming_service, get_image_tags_to_retain, \
    apply_image_cleanup_job, get_pod_name_corresponing_to_job, get_pod_status_from_job \


from tensorkube.helpers import  sanitise_name, \
    track_event, extract_command_from_dockerfile, extract_workdir_from_dockerfile

from tensorkube.services.knative_service import apply_knative_service_with_podman, apply_virtual_service_for_routing

from tensorkube.constants import Events, DEFAULT_NAMESPACE, BUILD_TOOL, PodStatus, \
    CliColors

from tensorkube.services.environment_service import check_environment_exists
from tensorkube.services.k8s_service import list_secrets

from tensorkube.services.aws_service import  get_credentials, get_bucket_name

from tensorkube.services.aws_service import get_aws_account_id, get_credentials, get_bucket_name, get_aws_user_arn, \
    are_credentials_valid

from tensorkube.services.s3_service import create_s3_bucket, delete_s3_bucket, upload_files_in_parallel, empty_s3_folder

from tensorkube.services.ecr_service import get_or_create_ecr_repository
from typing import Optional

DEFAULT_GPUS = 0
DEFAULT_GPU_TYPE = None
DEFAULT_CPU = 100
DEFAULT_MEMORY = 200
DEFAULT_MIN_SCALE = 0
DEFAULT_MAX_SCALE = 3
DEFAULT_GITHUB_ACTIONS = False
DEFAULT_ENV = None
DEFAULT_SECRET = None


class Config(object):
    def __init__(self, config_file_path):
        self.__config = {}
        if config_file_path != None:
            file_path = os.path.abspath(config_file_path)  # Convert to absolute path
            if not os.path.isfile(file_path):
                raise Exception(f"Config.yaml file not found in path: {file_path}")
            with open(file_path, 'r') as config_file:
                self.__config = yaml.safe_load(config_file)
        

    def get(self, key):
        return self.__config.get(key, None)

    def set_if_not_exist(self, key, value):
        if key in self.__config:
            return self
        if isinstance(value, tuple):
            self.__config[key] = list(value)
        else:
            self.__config[key] = value
        return self
        
    def __str__(self) -> str:
        return str(self.__config)
    

def upload_build_context_to_s3(bucket_name, sanitised_project_name, cwd):
    # TODO: figure out how to upload only the updated files to the s3 bucket
    click.echo("Deleting any outdated files in the S3 bucket...")
    empty_s3_folder(bucket_name=bucket_name, folder_name="build/" + sanitised_project_name + "/")

    click.echo("Uploading the current directory to the S3 bucket...")
    upload_files_in_parallel(bucket_name=bucket_name, folder_path=cwd,
                                s3_path="build/" + sanitised_project_name + "/")


def create_deployment_details(secret: list, env: str):
    secrets = [s for s in secret]
    if env and not check_environment_exists(env_name=env):
        click.echo("Environment does not exist. Please create the environment first.")
        return None, None, None, None, None
    env_namespace = DEFAULT_NAMESPACE if not env else env
    if secrets:
        secrets_list = list_secrets(env_namespace)
        secrets_names_list = [secret.metadata.name for secret in secrets_list]
        for secret in secrets:
            if secret not in secrets_names_list:
                click.echo(click.style("Secret ", fg=CliColors.ERROR.value)
                           + click.style(secret, fg=CliColors.ERROR.value, bold=True, italic=True)
                           + click.style(" not found in the environment.", fg=CliColors.ERROR.value))
                return None, None, None, None, None

    image_tag = uuid.uuid4().hex
    cwd = os.getcwd()
    non_sanitised_name = os.path.basename(cwd)
    sanitised_project_name = sanitise_name(non_sanitised_name)

    return secrets, env_namespace, image_tag, cwd, sanitised_project_name

    
def build_app(env, sanitised_project_name, image_tag, upload_to_nfs:bool=False,image_url:Optional[str]=None, work_dir:str = os.getcwd()):
    is_dockerfile_present = False
    for root, dirs, files in os.walk(work_dir):
        for file in files:
            local_file = os.path.join(root, file)
            if local_file == work_dir + "/Dockerfile":
                is_dockerfile_present = True
    
    if not is_dockerfile_present:
        click.echo("No Dockerfile found in current directory.")
        return
    
    
    bucket_name = get_bucket_name(env_name=env)
    
    build_job_name = f'{BUILD_TOOL}-{sanitised_project_name}'
    old_cleanup_job = 'cleanup-{}'.format(sanitised_project_name)

    env_namespace = DEFAULT_NAMESPACE if not env else env
    old_job_deleted = find_and_delete_old_job(job_name=build_job_name, namespace=env_namespace)
    old_cleanup_job_del = find_and_delete_old_job(job_name=old_cleanup_job, namespace=env_namespace)
    if not old_job_deleted:
        click.echo("Another deployment is already in progress. Please wait for the build to complete.")
        return

    # TODO!: add logic to update the aws-secret only if IAM Identity Center User
    credentials = get_credentials()
    if are_credentials_valid(credentials):
        click.echo("Credentials are up to date")
    else:
        click.echo("The AWS credentials have expired. Please update the credentials.")
        return
    upload_build_context_to_s3(bucket_name=bucket_name, sanitised_project_name=sanitised_project_name, cwd=work_dir)    
    click.echo("Building the Docker image...")
    
    apply_k8s_buildkit_config(sanitised_project_name=sanitised_project_name, image_tag=image_tag, env_name=env, image_url=image_url, upload_to_nfs=upload_to_nfs)
    build_job_pod_name = get_pod_name_corresponing_to_job(job_name=build_job_name, namespace=env_namespace)

    # TODO: stream multiple lines instead of one by one
    start_streaming_pod(pod_name=build_job_pod_name, namespace=env_namespace, status=PodStatus.SUCCEEDED)

    transition_time = time.time()
    # wait for the pod to transition
    while True:
        try:
            pod_status = check_pod_status(pod_name=build_job_pod_name, namespace=env_namespace)
        except client.ApiException as e:
            if e.status == 404:
                print('Pod not found.')
                pod_status = get_pod_status_from_job(job_name=build_job_name, namespace=env_namespace)
            else:
                pod_status = PodStatus.FAILED.value
        print('Waiting for pod to transition')
        if pod_status in ['Succeeded', 'Completed', 'Failed']:
            break
        if time.time() - transition_time > 60:  # 60 seconds have passed
            print("Timeout: Pod did not reach the desired state within 1 minute.")
            break
        time.sleep(5)
    return pod_status


def deploy_knative_service(env: str, gpus: int, gpu_type: str, cpu: float, memory: float, min_scale: int, max_scale: int,
                           pod_status: str, cwd: str, sanitised_project_name: str, image_tag: str, secrets: list):
    env_namespace = DEFAULT_NAMESPACE if not env else env

    if pod_status == 'Succeeded' or pod_status == 'Completed':
        click.echo("Successfully built and pushed the Docker image.")
        yaml_file_path = resource_filename('tensorkube', 'configurations/build_configs/knative_base_config.yaml')
        dockerfile_path = cwd + "/Dockerfile"
        workdir = extract_workdir_from_dockerfile(dockerfile_path)
        command = extract_command_from_dockerfile(dockerfile_path)
        service_name = f"{sanitised_project_name}-gpus-{gpus}-{str(gpu_type).lower()}"
        apply_knative_service_with_podman(service_name=service_name, yaml_file_path=yaml_file_path,
                                            sanitised_project_name=sanitised_project_name, image_tag=image_tag,
                                            workdir=workdir, command=command, gpus=gpus, gpu_type=gpu_type, cpu=cpu,
                                            memory=memory, min_scale=min_scale, max_scale=max_scale, env=env,
                                            secrets=secrets)
        virtual_service_yaml_file_path = resource_filename('tensorkube',
                                                            'configurations/build_configs/virtual_service.yaml')
        apply_virtual_service_for_routing(service_name=service_name, yaml_file_path=virtual_service_yaml_file_path,
                                            env=env, sanitised_project_name=sanitised_project_name)
        # click.echo(
        #     f"The service {service_name} sent for deployment. Waiting for it to become ready. Time taken: {(end_time - start_time) / 1000} ms.")
        images_to_retain = get_image_tags_to_retain(sanitised_project_name=sanitised_project_name,
                                                    service_name=service_name, namespace=env_namespace)
        apply_image_cleanup_job(sanitised_project_name=sanitised_project_name, image_tags=images_to_retain, env=env)
        start_streaming_service(service_name=service_name, namespace=env_namespace)
    else:
        click.echo(
            "Failed to build the Docker image. Please check the logs for more details. Pod status: {}".format(
                pod_status))
