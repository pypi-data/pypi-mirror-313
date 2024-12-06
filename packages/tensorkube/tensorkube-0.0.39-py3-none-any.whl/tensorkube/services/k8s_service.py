import subprocess
import time
from threading import Thread
from typing import List, Optional, Dict, Any

import click
import yaml
from kubernetes import client, config, utils, watch
from kubernetes.client import ApiTypeError, ApiException
from pkg_resources import resource_filename

from tensorkube.constants import NAMESPACE, REGION, PodStatus, BUILD_TOOL, DEFAULT_NAMESPACE, TENSORFUSE_NAMESPACES, \
    get_cluster_name, CliColors
from tensorkube.services.aws_service import get_aws_account_id
import json
import boto3
import os

def get_s3_pv_name(env_name: Optional[str] = None):
    if env_name:
        return f"s3-pv-env-{env_name}"
    return "s3-pv"


def get_s3_claim_name(env_name: Optional[str] = None):
    if env_name:
        return f"s3-claim-env-{env_name}"
    return "s3-claim"


def get_efs_claim_name(env_name: Optional[str] = None):
    if env_name:
        return f"efs-pvc-env-{env_name}"
    return "efs-pvc"


def create_namespace(namespace_name, context_name: Optional[str] = None):
    if not context_name:
        context_name = get_tensorkube_cluster_context_name()
        if not context_name:
            return None
    k8s_api_client = config.new_client_from_config(context=context_name)
    namespace = client.V1Namespace()
    namespace.metadata = client.V1ObjectMeta(name=namespace_name)
    v1 = client.CoreV1Api(k8s_api_client)
    v1.create_namespace(body=namespace)


def create_docker_registry_secret(secret_name: str, namespace: str, base64_encoded_dockerconfigjson: str,
                                  context_name: Optional[str] = None):
    if not context_name:
        context_name = get_tensorkube_cluster_context_name()
        if not context_name:
            return None
    k8s_api_client = config.new_client_from_config(context=context_name)
    v1 = client.CoreV1Api(k8s_api_client)

    secret = client.V1Secret()
    secret.api_version = "v1"
    secret.kind = "Secret"
    secret.metadata = client.V1ObjectMeta(name=secret_name, namespace=namespace)
    secret.type = "kubernetes.io/dockerconfigjson"
    secret.data = {".dockerconfigjson": base64_encoded_dockerconfigjson}

    v1.create_namespaced_secret(namespace=namespace, body=secret)


def create_aws_secret(credentials, namespace: str = DEFAULT_NAMESPACE, context_name: Optional[str] = None):
    if not context_name:
        context_name = get_tensorkube_cluster_context_name()
        if not context_name:
            return None
    k8s_api_client = config.new_client_from_config(context=context_name)
    v1 = client.CoreV1Api(k8s_api_client)
    secret_name = "aws-secret"

    secret = client.V1Secret()
    secret.metadata = client.V1ObjectMeta(name=secret_name)
    secret.string_data = {"AWS_ACCESS_KEY_ID": credentials.access_key, "AWS_SECRET_ACCESS_KEY": credentials.secret_key,
                          "AWS_SESSION_TOKEN": credentials.token}

    try:
        # Check if the secret already exists
        existing_secret = v1.read_namespaced_secret(name=secret_name, namespace=namespace)
        # If the secret exists, update it
        v1.replace_namespaced_secret(name=secret_name, namespace=namespace, body=secret)
        print(f"Secret {secret_name} updated successfully in namespace {namespace}.")
    except ApiException as e:
        if e.status == 404:
            # Secret does not exist, create it
            v1.create_namespaced_secret(namespace=namespace, body=secret)
            print(f"Secret {secret_name} created successfully in namespace {namespace}.")
        else:
            print(f"An error occurred: {e}")
            raise e


def delete_aws_secret(namespace: str = DEFAULT_NAMESPACE, context_name: Optional[str] = None):
    if not context_name:
        context_name = get_tensorkube_cluster_context_name()
        if not context_name:
            return None
    k8s_api_client = config.new_client_from_config(context=context_name)
    v1 = client.CoreV1Api(k8s_api_client)
    try:
        v1.read_namespaced_secret(name="aws-secret", namespace=namespace)
    except client.ApiException as e:
        if e.status == 404:
            return
        else:
            raise
    v1.delete_namespaced_secret(name="aws-secret", namespace=namespace)


def create_build_pv_and_pvc(bucket_name: str, region: str = REGION, env: Optional[str] = None,
                            context_name: Optional[str] = None):
    if not context_name:
        context_name = get_tensorkube_cluster_context_name()
        if not context_name:
            return None
    k8s_api_client = config.new_client_from_config(context=context_name)

    pv_config_file_path = resource_filename('tensorkube', 'configurations/build_configs/pv.yaml')
    pvc_config_file_path = resource_filename('tensorkube', 'configurations/build_configs/pvc.yaml')
    with open(pv_config_file_path) as f:
        pv = yaml.safe_load(f)
    with open(pvc_config_file_path) as f:
        pvc = yaml.safe_load(f)

    env_namespace = env if env else DEFAULT_NAMESPACE

    pv['spec']['mountOptions'] = ["allow-delete", "region {}".format(region)]
    pv['spec']['csi']['volumeAttributes']['bucketName'] = bucket_name
    pv['metadata']['namespace'] = env_namespace
    pv['metadata']['name'] = get_s3_pv_name(env_name=env)

    pvc['metadata']['namespace'] = env_namespace
    pvc['metadata']['name'] = get_s3_claim_name(env_name=env)
    pvc['spec']['volumeName'] = get_s3_pv_name(env_name=env)

    v1 = client.CoreV1Api(k8s_api_client)

    pv_name = pv['metadata']['name']
    pvc_name = pvc['metadata']['name']

    try:
        # Check if the PV already exists
        v1.read_persistent_volume(name=pv_name)
        click.echo(f"PersistentVolume {pv_name} already exists. Skipping creation.")
    except ApiException as e:
        if e.status == 404:
            utils.create_from_dict(k8s_api_client, pv)
            click.echo(f"PersistentVolume {pv_name} created successfully.")
        else:
            click.echo(f"An error occurred while checking PersistentVolume: {e}")
            raise e

    try:
        # Check if the PVC already exists
        v1.read_namespaced_persistent_volume_claim(name=pvc_name, namespace=env_namespace)
        click.echo(f"PersistentVolumeClaim {pvc_name} already exists in namespace {env_namespace}. Skipping creation.")
    except ApiException as e:
        if e.status == 404:
            # PVC does not exist, proceed to create
            utils.create_from_dict(k8s_api_client, pvc)
            click.echo(f"PersistentVolumeClaim {pvc_name} created successfully in namespace {env_namespace}.")
        else:
            click.echo(f"An error occurred while checking PersistentVolumeClaim: {e}")
            raise e



def get_buildkit_command(sanitised_project_name: str, image_tag: str, image_url: Optional[str] =None, upload_to_nfs: bool= False, region: str = REGION):
    aws_account_number =  get_aws_account_id()
    command = [ "/bin/sh", "-c",
        f"""
        apk add --no-cache curl unzip aws-cli docker
        aws ecr get-login-password --region {region} | docker login --username AWS --password-stdin {aws_account_number}.dkr.ecr.{region}.amazonaws.com
        buildctl-daemonless.sh build\
            --frontend dockerfile.v0\
            --local context=/data/build/{sanitised_project_name}\
            --local dockerfile=/data/build/{sanitised_project_name}\
            --output type=image,name={image_url},push=true\
        """
    ]

    if upload_to_nfs:
        command =  ["/bin/sh", "-c", f"""
        mkdir -p /data/cache
        mkdir -p /test/tars/{sanitised_project_name} /mnt/efs/images/{sanitised_project_name}/{image_tag}/rootfs /test/tars/{sanitised_project_name} /test/images/{sanitised_project_name}/rootfs
        time buildctl-daemonless.sh build\
            --frontend dockerfile.v0\
            --local context=/data/build/{sanitised_project_name}\
            --local dockerfile=/data/build/{sanitised_project_name}\
            --output type=tar,dest=/test/tars/{sanitised_project_name}/{sanitised_project_name}-{image_tag}.tar
        if [ $? -ne 0 ]; then
            echo "buildctl-daemonless.sh command failed"
            exit 1
        fi
        echo "Extracting rootfs from tar file"
        time tar -xf /test/tars/{sanitised_project_name}/{sanitised_project_name}-{image_tag}.tar -C /test/images/{sanitised_project_name}/rootfs --checkpoint=1000 --checkpoint-action=echo="Extracted #%u: %T"
        if [ $? -ne 0 ]; then
            echo "extracting rootfs from tar file failed"
            exit 1
        fi
        echo "Extracted rootfs from tar file"
        echo "Uploading rootfs to NFS"
        cd /test/images/{sanitised_project_name}/rootfs
        find . -type d | split -l 5000 - batch_dir_
        find . -type f | split -l 5000 - batch_file_
        find . -type l | split -l 5000 - batch_link_

        total_batches=$(ls batch_* | wc -l)
        processed_batches=0
        total_time=0

        process_batches() {{
            local batch_type=$1
            for batch_file in batch_${{batch_type}}_*; do
                start_time=$(date +%s)
                
                if [ "$batch_type" == "dir" ]; then
                    cat $batch_file | parallel -j 15 mkdir -p /mnt/efs/images/{sanitised_project_name}/{image_tag}/rootfs/{{}}
                elif [ "$batch_type" == "file" ]; then
                    cat $batch_file | parallel -j 15 cp --parents {{}} /mnt/efs/images/{sanitised_project_name}/{image_tag}/rootfs/
                elif [ "$batch_type" == "link" ]; then
                    cat $batch_file | parallel -j 15 cp --parents -P {{}} /mnt/efs/images/{sanitised_project_name}/{image_tag}/rootfs/
                fi
                
                end_time=$(date +%s)
                batch_time=$((end_time - start_time))
                total_time=$((total_time + batch_time))
                processed_batches=$((processed_batches + 1))
                remaining_batches=$((total_batches - processed_batches))
                avg_time_per_batch=$((total_time / processed_batches))
                estimated_remaining_time=$((avg_time_per_batch * remaining_batches))
                
                echo "Processed batch $processed_batches/$total_batches. Remaining: $remaining_batches. Time for this batch: $batch_time seconds. Estimated remaining time: $estimated_remaining_time seconds."
                rm $batch_file
            done
        }}

        process_batches "dir"
        process_batches "file"
        process_batches "link"
        echo "Uploaded rootfs to NFS" """]
    return command

        

def apply_k8s_buildkit_config(sanitised_project_name: str, image_tag: str, region: str = REGION,
                              env_name: Optional[str] = None, context_name: Optional[str] = None, image_url: Optional[str] = None, upload_to_nfs: bool = False):
    if not context_name:
        context_name = get_tensorkube_cluster_context_name()
        if not context_name:
            return None
    k8s_api_client = config.new_client_from_config(context=context_name)

    buildkit_config_file_path = resource_filename('tensorkube', 'configurations/build_configs/buildkit.yaml')
    with open(buildkit_config_file_path) as f:
        buildkit_config = yaml.safe_load(f)

    buildkit_config['metadata']['name'] = 'buildkit-{}'.format(sanitised_project_name)
    buildkit_config['spec']['template']['spec']['containers'][0]['env'][0]['value'] = region
    buildkit_config['spec']['ttlSecondsAfterFinished'] = 100

    # Include the namespace in the buildkit configuration
    # Replace 'default' with your default namespace if needed
    namespace_to_use = env_name if env_name else DEFAULT_NAMESPACE
    buildkit_config['metadata']['namespace'] = namespace_to_use

    # Modify volume claim names based on env_name
    for volume in buildkit_config['spec']['template']['spec']['volumes']:
        if volume['name'] == 'persistent-storage':
            volume['persistentVolumeClaim']['claimName'] = get_s3_claim_name(env_name=env_name)
        elif volume['name'] == 'efs-pvc':
            volume['persistentVolumeClaim']['claimName'] = get_efs_claim_name(env_name=env_name)

    buildkit_config['spec']['template']['spec']['containers'][0]['command'] = get_buildkit_command(sanitised_project_name, image_tag, image_url, upload_to_nfs, region)

    utils.create_from_dict(k8s_api_client, buildkit_config)
    click.echo('Deployed a Buildkit image')


def apply_image_cleanup_job(sanitised_project_name: str, image_tags: List[str], env: Optional[str] = None,
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

    for volume in cleanup_config['spec']['template']['spec']['volumes']:
        if volume['name'] == 'efs-pvc':
            volume['persistentVolumeClaim']['claimName'] = get_efs_claim_name(env_name=env)

    cleanup_config['spec']['template']['spec']['containers'][0]['command'] = ["/bin/sh", "-c",
                                                                              f"""cd /mnt/efs/images/{sanitised_project_name}
        echo 'Deleting all images except' {", ".join(image_tags)}
        find . -mindepth 1 -maxdepth 1 -type d ! -name {" ! -name ".join(image_tags)} -exec rm -rf {{}} +
        echo 'Deletion completed' """]

    utils.create_from_dict(k8s_api_client, cleanup_config)
    click.echo('Deployed a delete config job')


def get_build_job_pod_name(sanitised_project_name: str, namespace: str = NAMESPACE, context_name: Optional[str] = None):
    if not context_name:
        context_name = get_tensorkube_cluster_context_name()
        if not context_name:
            return None
    k8s_api_client = config.new_client_from_config(context=context_name)
    v1 = client.CoreV1Api(k8s_api_client)
    pods = v1.list_namespaced_pod(namespace=namespace)
    for pod in pods.items:
        if pod.metadata.name.startswith("{}-{}".format(BUILD_TOOL, sanitised_project_name)):
            return pod.metadata.name
    return None


def check_pod_status(pod_name, namespace, context_name: Optional[str] = None):
    # Load kube config
    if not context_name:
        context_name = get_tensorkube_cluster_context_name()
        if not context_name:
            return None
    k8s_api_client = config.new_client_from_config(context=context_name)

    # Create a Kubernetes API client
    v1 = client.CoreV1Api(k8s_api_client)

    # Get the status of the pod
    pod_status = v1.read_namespaced_pod_status(name=pod_name, namespace=namespace)

    # Return the status of the pod
    return pod_status.status.phase


def find_and_delete_old_job(job_name: str, namespace: str = DEFAULT_NAMESPACE, context_name: Optional[str] = None):
    if not context_name:
        context_name = get_tensorkube_cluster_context_name()
        if not context_name:
            return None
    k8s_api_client = config.new_client_from_config(context=context_name)
    v1 = client.CoreV1Api(k8s_api_client)
    job_pod_name = get_pod_name_corresponing_to_job(job_name, namespace)
    if job_pod_name:
        click.echo("Terminating pod {} corresponding to job {}".format(job_pod_name, job_name))
        v1.delete_namespaced_pod(name=job_pod_name, namespace=namespace)

    v1 = client.BatchV1Api(k8s_api_client)
    jobs = v1.list_namespaced_job(namespace=namespace)
    for job in jobs.items:
        if job.metadata.name == job_name:
            v1.delete_namespaced_job(name=job.metadata.name, namespace=namespace)
            return True

    return True


def delete_all_jobs_in_namespace(namespace: str, context_name: Optional[str] = None):
    if not context_name:
        context_name = get_tensorkube_cluster_context_name()
        if not context_name:
            return None
    k8s_api_client = config.new_client_from_config(context=context_name)
    v1 = client.BatchV1Api(k8s_api_client)
    jobs = v1.list_namespaced_job(namespace=namespace)
    for job in jobs.items:
        v1.delete_namespaced_job(name=job.metadata.name, namespace=namespace)
        print(f"Job {job.metadata.name} deletion initiated.")

        # Wait for the job to be deleted
        while True:
            try:
                v1.read_namespaced_job(name=job.metadata.name, namespace=namespace)
                time.sleep(1)  # Wait for 1 second before checking again
            except ApiException as e:
                if e.status == 404:
                    print(f"Job {job.metadata.name} deleted successfully.")
                    break
                else:
                    print(f"Error while waiting for deletion of job {job.metadata.name}: {e}")
                    raise e
    return True


def start_streaming_pod(pod_name, namespace, status=None, container_name=None, retry_number: int = 0,
                        max_retries: int = 4, context_name: Optional[str] = None):
    if not context_name:
        context_name = get_tensorkube_cluster_context_name()
        if not context_name:
            return None
    k8s_api_client = config.new_client_from_config(context=context_name)
    v1 = client.CoreV1Api(k8s_api_client)
    # Create a stream to the pod
    # Initialize the Watch class
    watch_client = watch.Watch()
    # Stream events until the pod is ready
    print(f"Streaming events for pod {pod_name} in namespace {namespace}")
    try:
        events_streamed_upto_index = 0

        while True:
            pod = v1.read_namespaced_pod(name=pod_name, namespace=namespace)
            events = v1.list_namespaced_event(namespace=namespace, field_selector=f'involvedObject.name={pod_name}')
            for event in events.items[events_streamed_upto_index:]:
                print("Event: %s %s" % (event.type, event.message))
            events_streamed_upto_index = len(events.items)
            if pod.status.phase != 'Pending':
                break
            time.sleep(1)

    except KeyboardInterrupt:
        print("Log streaming stopped by user")
        return

    print(f"Streaming logs for pod {pod_name} in namespace {namespace}")

    try:
        last_log_printed = None
        while True:
            logs = v1.read_namespaced_pod_log(name=pod_name, namespace=namespace, container=container_name,
                                              since_seconds=5)
            logs_by_line = logs.split('\n')
            logs_by_line = logs_by_line[:len(logs_by_line) - 1]
            if logs_by_line:
                if not last_log_printed:
                    for log in logs_by_line:
                        print(log)
                else:
                    found_last_printed_log = False
                    for log in logs_by_line:
                        if found_last_printed_log:
                            print(log)
                            continue
                        if log == last_log_printed:
                            found_last_printed_log = True
                            continue
                        continue
                    if not found_last_printed_log:
                        for log in logs_by_line:
                            print(log)
                last_log_printed = logs_by_line[-1]

            pod = v1.read_namespaced_pod_status(name=pod_name, namespace=namespace)
            if pod.status.phase == PodStatus.FAILED.value:
                print(f"Pod {pod_name} in namespace {namespace} failed.")
                return
            if status:
                if status.value == pod.status.phase:
                    print(f"Pod {pod_name} has reached {status.value} state")
                    return
            time.sleep(1)
    except client.ApiException as e:
        if e.status == 404:
            print(f"Pod {pod_name} not found in namespace {namespace}")
        else:
            raise
    except KeyboardInterrupt:
        print("Log streaming stopped by user")
        return
    except ApiTypeError as e:
        print(f"An error occurred while streaming logs for pod {pod_name} in namespace {namespace}")
        print(e)
        return
    except Exception as e:
        print(f"An unexpected error occurred for pod {pod_name} in namespace {namespace}")
        print(e)
        raise


def get_pod_status_from_job(job_name: str, namespace: str = DEFAULT_NAMESPACE, context_name: str = None) -> Optional[
    str]:
    if not context_name:
        context_name = get_tensorkube_cluster_context_name()
        if not context_name:
            return None
    k8s_api_client = config.new_client_from_config(context=context_name)
    v1 = client.BatchV1Api(k8s_api_client)
    try:
        job = v1.read_namespaced_job(name=job_name, namespace=namespace)
        if job.status.failed == 1:
            return PodStatus.FAILED.value
        if job.status.succeeded == 1:
            return PodStatus.SUCCEEDED.value
        return None
    except ApiException as e:
        if e.status == 404:
            print(f"Job {job_name} not found in namespace {namespace}")
            return PodStatus.FAILED.value
        else:
            raise e


def start_streaming_service(service_name, namespace, context_name: Optional[str] = None):
    # Load kube config
    if not context_name:
        context_name = get_tensorkube_cluster_context_name()
        if not context_name:
            return None
    k8s_api_client = config.new_client_from_config(context=context_name)

    # Create a Kubernetes API client
    v1 = client.CoreV1Api(k8s_api_client)

    # Stream the service status
    try:
        while True:
            pods = v1.list_namespaced_pod(namespace, label_selector=f'serving.knative.dev/service={service_name}')
            if pods.items:
                sorted_pods = sorted(pods.items, key=lambda x: x.metadata.name, reverse=True)
                print(f"Pods scheduled for service {service_name}: {sorted_pods[0].metadata.name}")
                break
            time.sleep(5)
        # Start streaming the logs from the pod
        thread = Thread(target=start_streaming_pod,
                        args=(sorted_pods[0].metadata.name, namespace, PodStatus.RUNNING, 'user-container'))
        thread.start()
    except client.ApiException as e:
        if e.status == 404:
            print(f"Service {service_name} not found in namespace {namespace}")
        else:
            raise
    except KeyboardInterrupt:
        print("Service status streaming stopped by user")
        return
    except Exception as e:
        print("An unexpected error occurred for service status streaming")
        raise


def check_nodes_ready(label_selector):
    context_name = get_tensorkube_cluster_context_name()
    if not context_name:
        return None
    k8s_api_client = config.new_client_from_config(context=context_name)
    v1 = client.CoreV1Api(k8s_api_client)
    ready_nodes = []
    nodes = v1.list_node(label_selector=label_selector).items
    for node in nodes:
        for condition in node.status.conditions:
            if condition.type == "Ready" and condition.status == "True":
                ready_nodes.append(node.metadata.name)
    return len(ready_nodes) == len(nodes), ready_nodes


def evict_pods_from_node(node_name, context_name: Optional[str] = None):
    if not context_name:
        context_name = get_tensorkube_cluster_context_name()
        if not context_name:
            return None
    k8s_api_client = config.new_client_from_config(context=context_name)
    core_api = client.CoreV1Api(k8s_api_client)
    pods = core_api.list_pod_for_all_namespaces(field_selector=f'spec.nodeName={node_name}').items
    for pod in pods:
        if pod.metadata.owner_references and any(owner.kind == "DaemonSet" for owner in pod.metadata.owner_references):
            continue
        eviction = client.V1Eviction(
            metadata=client.V1ObjectMeta(name=pod.metadata.name, namespace=pod.metadata.namespace))
        retry_attempts = 0
        max_retries = 5
        backoff_delay = 1  # Start with 1 second delay
        while retry_attempts < max_retries:
            try:
                core_api.create_namespaced_pod_eviction(name=pod.metadata.name, namespace=pod.metadata.namespace,
                                                        body=eviction)
                print(f"Evicting pod {pod.metadata.name} from node {node_name}.")
                break  # Eviction successful, break out of the retry loop
            except ApiException as e:
                if e.status == 429:  # Too Many Requests
                    print(
                        f"Rate limit exceeded when evicting pod {pod.metadata.name}: {e}. Retrying in {backoff_delay} seconds...")
                    time.sleep(backoff_delay)
                    backoff_delay *= 2  # Exponential backoff
                    retry_attempts += 1
                else:
                    print(f"Exception when evicting pod {pod.metadata.name}: {e}")
                    break  # Break on any other exception
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                break
        if retry_attempts == max_retries:
            print(f"Failed to evict pod {pod.metadata.name} after {max_retries} attempts.")


def drain_and_delete_node(node_name, context_name: Optional[str] = None):
    if not context_name:
        context_name = get_tensorkube_cluster_context_name()
        if not context_name:
            return None
    k8s_api_client = config.new_client_from_config(context=context_name)
    core_api = client.CoreV1Api(k8s_api_client)
    # Cordon the node
    body = {"spec": {"unschedulable": True}}
    core_api.patch_node(node_name, body)
    click.echo(f"Cordoned node {node_name}")

    # Evict all pods from the node
    evict_pods_from_node(node_name)
    click.echo(f"All pods evicted from node {node_name}")

    # delete the node
    core_api.delete_node(node_name)


def get_nodes_not_using_bottlerocket(ec2_node_class_label, context_name: Optional[str] = None):
    if not context_name:
        context_name = get_tensorkube_cluster_context_name()
        if not context_name:
            return None
    k8s_api_client = config.new_client_from_config(context=context_name)
    v1 = client.CoreV1Api(k8s_api_client)

    # List all nodes
    nodes = v1.list_node().items

    filtered_nodes = []
    for node in nodes:
        labels = node.metadata.labels
        os_image = node.status.node_info.os_image

        # Check if the node belongs to the specified EC2NodeClass
        if labels.get('karpenter.sh/nodepool') == ec2_node_class_label:
            # Check if the node is using Bottlerocket AMI
            if 'bottlerocket' not in os_image.lower():
                filtered_nodes.append(node.metadata.name)

    return filtered_nodes


def delete_pv_using_name(pv_name: str, context_name: Optional[str] = None):
    if not context_name:
        context_name = get_tensorkube_cluster_context_name()
        if not context_name:
            return None
    k8s_api_client = config.new_client_from_config(context=context_name)
    v1 = client.CoreV1Api(k8s_api_client)

    timeout = 60  # Timeout in seconds
    start_time = time.time()

    try:
        v1.delete_persistent_volume(name=pv_name)
        while time.time() - start_time < timeout:
            try:
                v1.read_persistent_volume(name=pv_name)
                print(f"Waiting for PV {pv_name} to be deleted...")
                time.sleep(5)  # Wait for 5 seconds before checking again
            except ApiException as e:
                if e.status == 404:
                    print(f"PersistentVolume {pv_name} successfully deleted.")
                    return
                else:
                    raise
        print(f"Timeout reached while waiting for PV {pv_name} to be deleted.")
    except client.exceptions.ApiException as e:
        if e.status == 404:
            print(f"PersistentVolume {pv_name} not found")
        else:
            raise e


def delete_pvc_using_name_and_namespace(pvc_name: str, namespace: str, context_name: Optional[str] = None):
    if not context_name:
        context_name = get_tensorkube_cluster_context_name()
        if not context_name:
            return None
    k8s_api_client = config.new_client_from_config(context=context_name)
    v1 = client.CoreV1Api(k8s_api_client)
    timeout = 60  # Timeout in seconds
    start_time = time.time()
    try:
        v1.delete_namespaced_persistent_volume_claim(name=pvc_name, namespace=namespace)
        while time.time() - start_time < timeout:
            try:
                v1.read_namespaced_persistent_volume_claim(name=pvc_name, namespace=namespace)
                print(f"Waiting for PVC {pvc_name} to be deleted...")
                time.sleep(5)  # Wait for 5 seconds before checking again
            except ApiException as e:
                if e.status == 404:
                    print(f"PersistentVolumeClaim {pvc_name} successfully deleted from namespace {namespace}.")
                    return
                else:
                    raise
        print(f"Timeout reached while waiting for PVC {pvc_name} to be deleted.")
    except client.exceptions.ApiException as e:
        if e.status == 404:
            print(f"PersistentVolumeClaim {pvc_name} not found in namespace {namespace}")
        else:
            raise e


def check_pvc_exists_by_name(claim_name, namespace, context_name: Optional[str] = None):
    if not context_name:
        context_name = get_tensorkube_cluster_context_name()
        if not context_name:
            return None
    k8s_api_client = config.new_client_from_config(context=context_name)

    # Create an instance of the CoreV1Api
    v1 = client.CoreV1Api(k8s_api_client)

    try:
        # Attempt to read the specified PVC in the given namespace
        v1.read_namespaced_persistent_volume_claim(name=claim_name, namespace=namespace)
        return True  # PVC exists
    except ApiException as e:
        if e.status == 404:
            return False  # PVC does not exist
        else:
            print(f"An error occurred: {e}")
            raise e


def get_image_tags_to_retain(sanitised_project_name: str, service_name: str, namespace: str,
                             context_name: Optional[str] = None):
    if not context_name:
        context_name = get_tensorkube_cluster_context_name()
        if not context_name:
            return None
    k8s_api_client = config.new_client_from_config(context=context_name)
    k8s_client = client.CustomObjectsApi(k8s_api_client)
    click.echo(f"Cleaning up old image tags for project {sanitised_project_name}, service {service_name}.")
    group = "serving.knative.dev"
    version = "v1"
    plural = "revisions"

    # List all revisions for the service
    # Define the label selector string based on the service name
    label_selector = f"serving.knative.dev/service={service_name}"

    # Use the label selector in the list_namespaced_custom_object call to directly filter revisions
    service_revisions = \
        k8s_client.list_namespaced_custom_object(group, version, namespace, plural, label_selector=label_selector)[
            'items']

    # Sort all revisions by configurationGeneration in descending order
    all_revisions_sorted = sorted(service_revisions, key=lambda x: int(
        x['metadata']['labels']['serving.knative.dev/configurationGeneration']), reverse=True)

    # Identify all "Ready" revisions
    ready_revisions = [rev for rev in all_revisions_sorted if any(
        cond['type'] == 'Ready' and cond['status'] == 'True' for cond in rev['status']['conditions'])]

    # Find the index of the latest "Ready" revision
    if ready_revisions:
        latest_ready_revision = ready_revisions[0]
        latest_ready_index = all_revisions_sorted.index(latest_ready_revision)
    else:
        latest_ready_index = -1

    # Determine active revisions
    active_revisions = ready_revisions[:3]  # Last three "Ready" revisions
    if latest_ready_index != -1:
        active_revisions += all_revisions_sorted[:latest_ready_index]  # Any newer revisions

    # Find the index for slicing stale revisions
    if len(ready_revisions) >= 3:
        third_last_ready_index = all_revisions_sorted.index(ready_revisions[2])
    elif len(ready_revisions) == 2:
        third_last_ready_index = all_revisions_sorted.index(ready_revisions[1])
    else:
        third_last_ready_index = latest_ready_index

    # Determine stale revisions, ensuring last three "Ready" revisions are not included
    stale_revisions = all_revisions_sorted[third_last_ready_index + 1:] if third_last_ready_index != -1 else []
    retained_revisions = all_revisions_sorted[
                         :third_last_ready_index + 1] if third_last_ready_index != -1 else all_revisions_sorted

    image_tags_to_retain = []
    image_tags_to_delete = []
    for rev in retained_revisions:
        # check if this exists yaml_dict['spec']['template']['metadata']['annotations']['image_tag'] = image_tag
        if rev['metadata']['annotations'] and 'image_tag' in rev['metadata']['annotations']:
            image_tags_to_retain.append(rev['metadata']['annotations']['image_tag'])
            click.echo(f'Retaining revision {rev["metadata"]["name"]}')
        else:
            print(f'No image tag found for revision {rev["metadata"]["name"]}')

    for rev in stale_revisions:
        # check if this exists yaml_dict['spec']['template']['metadata']['annotations']['image_tag'] = image_tag
        if rev['metadata']['annotations'] and 'image_tag' in rev['metadata']['annotations']:
            image_tags_to_delete.append(rev['metadata']['annotations']['image_tag'])
            click.echo(f'Queuing revision {rev["metadata"]["name"]} for deletion')
        else:
            print(f'No image tag found for revision {rev["metadata"]["name"]}')
        try:
            # Delete the revision
            k8s_client.delete_namespaced_custom_object(group=group, version=version, namespace=namespace, plural=plural,
                                                       name=rev['metadata']['name'], body=client.V1DeleteOptions()
                                                       # You can customize this if needed
                                                       )
        except client.exceptions.ApiException as e:
            print(f"Failed to delete revision {rev['metadata']['name']}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while deleting revision {rev['metadata']['name']}: {e}")
    return image_tags_to_retain


def get_pod_name_corresponing_to_job(job_name: str, namespace: str = DEFAULT_NAMESPACE,
                                     context_name: Optional[str] = None) -> Optional[str]:
    if not context_name:
        context_name = get_tensorkube_cluster_context_name()
        if not context_name:
            return None
    k8s_api_client = config.new_client_from_config(context=context_name)
    v1 = client.CoreV1Api(k8s_api_client)
    pods = v1.list_namespaced_pod(namespace=namespace)

    for pod in pods.items:
        if not pod.metadata.owner_references:
            continue
        for owner in pod.metadata.owner_references:
            if owner.name == job_name:
                return pod.metadata.name

    return None


def create_new_namespace(env_name: str, context_name: Optional[str] = None):
    if not context_name:
        context_name = get_tensorkube_cluster_context_name()
        if not context_name:
            return None
    k8s_api_client = config.new_client_from_config(context=context_name)
    namespace = client.V1Namespace()
    namespace.metadata = client.V1ObjectMeta(name=env_name)
    v1 = client.CoreV1Api(k8s_api_client)
    v1.create_namespace(body=namespace)
    click.echo(f"Namespace {env_name} created successfully.")


def delete_namespace(env_name: str, context_name: Optional[str] = None):
    if env_name == DEFAULT_NAMESPACE or env_name in TENSORFUSE_NAMESPACES:
        click.echo(f"Cannot delete namespace {env_name}")
        return
    if not context_name:
        context_name = get_tensorkube_cluster_context_name()
        if not context_name:
            return None
    k8s_api_client = config.new_client_from_config(context=context_name)
    v1 = client.CoreV1Api(k8s_api_client)
    v1.delete_namespace(name=env_name)
    click.echo(f"Namespace {env_name} deleted successfully.")


def list_all_namespaces(context_name: Optional[str] = None):
    if not context_name:
        context_name = get_tensorkube_cluster_context_name()
        if not context_name:
            return None
    k8s_api_client = config.new_client_from_config(context=context_name)
    v1 = client.CoreV1Api(k8s_api_client)
    namespaces = v1.list_namespace().items
    return [namespace.metadata.name for namespace in namespaces]


def ssh_into_pod_with_podman(pod_name: str, namespace: str, context_name: Optional[str] = None):
    if not context_name:
        context_name = get_tensorkube_cluster_context_name()
        if not context_name:
            return None
    command = ["kubectl", "--context", f"{context_name}", "exec", "-it", pod_name, "-n", namespace, "-c",
               "user-container", "--", "sh", "-c", "podman exec -it $(podman ps -q) /bin/bash"]
    subprocess.run(command)


def get_tensorkube_cluster_context_name() -> Optional[str]:
    # Get the list of all contexts and the current context
    contexts, current_context = config.list_kube_config_contexts()

    tensorkube_contexts = [context['name'] for context in contexts if (
            f"cluster/{get_cluster_name()}" in context['name'] or f"@{get_cluster_name()}" in context['name'])]
    if len(tensorkube_contexts) == 1:
        return tensorkube_contexts[0]
    elif len(tensorkube_contexts) > 1:
        valid_context = remove_invalid_contexts(tensorkube_contexts)
        return valid_context
    else:
        click.echo(click.style(f"No context found for {get_cluster_name()} cluster.", fg="red"))
        click.echo(
            f"If you have already created a {get_cluster_name()} cluster and have access to it, please run the command")
        click.echo(click.style("tensorkube sync", fg="cyan"))
        click.echo("Otherwise, please create a new cluster using the command")
        click.echo(click.style("tensorkube configure", fg="cyan"))
        return None


def remove_invalid_contexts(tensorkube_contexts: List[str]) -> Optional[str]:
    for context in tensorkube_contexts:
        try:
            command = ["kubectl", "--context", f"{context}", "get", "pods"]
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError:
            command = ["kubectl", "config", "delete-context", context]
            subprocess.run(command)
            tensorkube_contexts.remove(context)

    if len(tensorkube_contexts) == 1:
        return tensorkube_contexts[0]
    elif len(tensorkube_contexts) > 1:
        return tensorkube_contexts[0]
    return None


def create_secret(name: str, namespace: str, data: Dict[str, str], force: bool = False, context_name: Optional[str] = None):
    if not context_name:
        context_name = get_tensorkube_cluster_context_name()
        if not context_name:
            raise Exception("No context found for the cluster. Please configure Tensorfuse properly.")
    k8s_api_client = config.new_client_from_config(context=context_name)
    v1 = client.CoreV1Api(k8s_api_client)
 
    secret = client.V1Secret()
    secret.metadata = client.V1ObjectMeta(name=name, namespace=namespace)
    secret.string_data = data


    try:
        # Check if the secret already exists
        v1.read_namespaced_secret(name, namespace)
        if force:
            # If the secret exists and force is True, update the secret
            v1.replace_namespaced_secret(name, namespace, body=secret)
            click.echo(click.style("Updated already existing secret ", fg=CliColors.SUCCESS.value) 
                       + click.style(name, bold=True, fg=CliColors.SUCCESS.value)
                       + click.style(" in namespace ", fg=CliColors.SUCCESS.value) 
                       + click.style(namespace, bold=True, fg=CliColors.SUCCESS.value))
        else:
            click.echo(click.style("Secret ", fg=CliColors.WARNING.value) 
                       + click.style(name,  bold=True, fg=CliColors.WARNING.value)
                       + click.style(" already exists in namespace ", fg=CliColors.WARNING.value)
                       + click.style(namespace, bold=True, fg=CliColors.WARNING.value)
                       + click.style(". Use --force to update the secret.", fg=CliColors.WARNING.value))
    except ApiException as e:
        if e.status == 404:
            # If the secret does not exist, create it
            try:
                v1.create_namespaced_secret(namespace=namespace, body=secret)
                click.echo(click.style("Secret ", fg=CliColors.SUCCESS.value) 
               + click.style(name, bold=True, fg=CliColors.SUCCESS.value)
               + click.style(" created successfully.", fg=CliColors.SUCCESS.value))
            except ApiException as e:
                click.echo(click.style("An error occurred while creating the secret", fg=CliColors.ERROR.value))
                click.echo(click.style(f"Error: {e}", fg=CliColors.ERROR.value))
        else:
            raise e

def list_secrets(namespace: str, context_name: Optional[str] = None):
    if not context_name:
        context_name = get_tensorkube_cluster_context_name()
        if not context_name:
            return []
    k8s_api_client = config.new_client_from_config(context=context_name)
    v1 = client.CoreV1Api(k8s_api_client)
    secrets = v1.list_namespaced_secret(namespace).items
    if not secrets:
        return []
    return secrets


def delete_secret(name: str, namespace: str, context_name: Optional[str] = None):
    if not context_name:
        context_name = get_tensorkube_cluster_context_name()
        if not context_name:
            return None
    k8s_api_client = config.new_client_from_config(context=context_name)
    v1 = client.CoreV1Api(k8s_api_client)
    try:
        v1.delete_namespaced_secret(name, namespace)
        click.echo(click.style("Secret ", fg=CliColors.SUCCESS.value) 
                   + click.style(name, bold=True, fg=CliColors.SUCCESS.value)
                   + click.style(" deleted successfully.", fg=CliColors.SUCCESS.value))
    except ApiException as e:
        if e.status == 404:
            click.echo(click.style("Secret ", fg=CliColors.WARNING.value) 
                       + click.style(name, bold=True, fg=CliColors.WARNING.value)
                       + click.style(" not found in namespace ", fg=CliColors.WARNING.value) 
                       + click.style(namespace, bold=True, fg=CliColors.WARNING.value))
        else:
            raise e


def create_configmap(name: str, namespace: str, data: Dict[str, str], force: bool = False, context_name: Optional[str] = None):
    if not context_name:
        context_name = get_tensorkube_cluster_context_name()
        if not context_name:
            raise Exception("No context found for the cluster. Please configure Tensorfuse properly.")
    k8s_api_client = config.new_client_from_config(context=context_name)
    v1 = client.CoreV1Api(k8s_api_client) 
    configmap = client.V1ConfigMap()
    configmap.metadata = client.V1ObjectMeta(name=name, namespace=namespace)
    configmap.data = {"config": yaml.dump(data)}
    try:
        # Check if the configmap already exists
        v1.read_namespaced_config_map(name, namespace)
        if force:
            # If the configmap exists and force is True, update the configmap
            v1.replace_namespaced_config_map(name, namespace, body=configmap)
    except ApiException as e:
        if e.status == 404:
            # If the configmap does not exist, create it
            try:
                v1.create_namespaced_config_map(namespace=namespace, body=configmap)
            except ApiException as e:
                raise e
        else:
            raise e

def get_pods_for_jobs(job_name: str, namespace: str = "default"):
    context_name = get_tensorkube_cluster_context_name()
    if not context_name:
        return None
    k8s_api_client = config.new_client_from_config(context=context_name)
    api = client.CoreV1Api(k8s_api_client)
    try:
        return api.list_namespaced_pod(
            namespace=namespace,
            label_selector=f"job-name={job_name}"
        )
    except ApiException as e:
        print(f"Exception when calling CoreV1Api->list_namespaced_pod: {e}")
        return None


def list_jobs(namespace: Optional[str] = None, all: bool = False,
              job_name_prefix: Optional[str] = None):
    """
    Lists Kubernetes jobs in a namespace or across all namespaces with optional job name prefix filtering

    Args:
        namespace: Specific namespace to list jobs from
        all: If True, lists jobs from all namespaces
        context_name: Kubernetes context name to use
        job_name_prefix: Optional prefix to filter job names

    Returns:
        Dict containing list of jobs or None if context not found
    """
    context_name = get_tensorkube_cluster_context_name()
    if not context_name:
        return None

    api_client = config.new_client_from_config(context=context_name)
    batch_v1 = client.BatchV1Api(api_client)

    try:
        if all:
            job_list = batch_v1.list_job_for_all_namespaces()
        else:
            namespace = namespace if namespace else DEFAULT_NAMESPACE
            job_list = batch_v1.list_namespaced_job(namespace=namespace)

        # Filter jobs by prefix if specified
        if job_name_prefix:
            filtered_items = [
                job for job in job_list.items
                if job.metadata.name.startswith(job_name_prefix)
            ]
            job_list.items = filtered_items

        return job_list
    except ApiException as e:
        print(f"Exception when calling BatchV1Api: {e}")
        return None


def delete_job(job_name: str, namespace: str = "default") -> bool:
    """
    Stops and deletes a Kubernetes job and its associated pods

    Args:
        job_name: Name of the job to delete
        namespace: Kubernetes namespace where the job exists

    Returns:
        bool: True if deletion was successful, False otherwise
    """
    try:
        # Get API clients
        api_client = config.new_client_from_config(context=get_tensorkube_cluster_context_name())
        batch_v1 = client.BatchV1Api(api_client)
        core_v1 = client.CoreV1Api(api_client)

        # First check if job exists
        try:
            batch_v1.read_namespaced_job(name=job_name, namespace=namespace)
        except ApiException as e:
            if e.status == 404:
                click.echo(click.style(f"Job {job_name} not found in namespace {namespace}", fg='red'))
                return False
            raise e

        # Delete associated pods first
        try:
            pods = core_v1.list_namespaced_pod(
                namespace=namespace,
                label_selector=f"job-name={job_name}"
            )
            for pod in pods.items:
                core_v1.delete_namespaced_pod(
                    name=pod.metadata.name,
                    namespace=namespace
                )
        except ApiException as e:
            print(f"Error deleting pods for job {job_name}: {e}")

        # Delete the job
        try:
            batch_v1.delete_namespaced_job(
                name=job_name,
                namespace=namespace,
                body=client.V1DeleteOptions(
                    propagation_policy='Foreground',
                    grace_period_seconds=0
                )
            )
            click.echo(click.style(f"Successfully deleted job {job_name}", fg='green'))
            return True
        except ApiException as e:
            click.echo(click.style(f"Error deleting job {job_name}: {e}", fg='red'))
            return False

    except Exception as e:
        print(f"Error in delete_job: {e}")
        click.echo(click.style(f"Failed to delete job: {str(e)}", fg='red'))
        return False


def list_keda_scaled_jobs():
    context_name = get_tensorkube_cluster_context_name()
    if not context_name:
        return None

    api_client = config.new_client_from_config(context=context_name)
    k8s_client = client.CustomObjectsApi(api_client)

    try:
        keda_scaled_jobs = k8s_client.list_namespaced_custom_object(
            group="keda.sh",
            version="v1alpha1",
            plural="scaledjobs",
            namespace="keda"
        )
        return keda_scaled_jobs
    except ApiException as e:
        print(f"Exception when calling CustomObjectsApi: {e}")
        return None


def list_trigger_authentications():
    context_name = get_tensorkube_cluster_context_name()
    if not context_name:
        return None

    api_client = config.new_client_from_config(context=context_name)
    k8s_client = client.CustomObjectsApi(api_client)

    try:
        trigger_authentications = k8s_client.list_namespaced_custom_object(
            group="keda.sh",
            version="v1alpha1",
            plural="triggerauthentications",
            namespace="keda"
        )
        return trigger_authentications
    except ApiException as e:
        print(f"Exception when calling CustomObjectsApi: {e}")
        return None


def delete_trigger_authentication(trigger_auth_name: str):
    context_name = get_tensorkube_cluster_context_name()
    if not context_name:
        return None

    api_client = config.new_client_from_config(context=context_name)
    k8s_client = client.CustomObjectsApi(api_client)

    try:
        k8s_client.delete_namespaced_custom_object(
            group="keda.sh",
            version="v1alpha1",
            plural="triggerauthentications",
            namespace="keda",
            name=trigger_auth_name
        )
    except ApiException as e:
        print(f"Exception when calling CustomObjectsApi: {e}")
        return None

def add_user_to_aws_auth_group(user_name, group_name):
    v1 = client.CoreV1Api()
    # details of the aws-auth ConfigMap
    namespace = "kube-system"
    configmap_name = "aws-auth"

    configmap = v1.read_namespaced_config_map(configmap_name, namespace)
    map_users = yaml.safe_load(configmap.data.get("mapUsers", "[]"))
    # Append the new user to the mapUsers list
    new_user = {
        "userarn": f"arn:aws:iam::{get_aws_account_id()}:user/{user_name}",
        "username": user_name,
        "groups": [group_name]
    }

    map_users.append(new_user)
    # Update the mapUsers back into the ConfigMap data
    configmap.data["mapUsers"] = yaml.dump(map_users)

    # Update the ConfigMap with the new user
    v1.replace_namespaced_config_map(name=configmap_name, namespace=namespace, body=configmap)


def add_user_to_k8s(user_name):
    config.load_kube_config()
    rbac_api = client.RbacAuthorizationV1Api()
    cluster_role_name = f"{get_cluster_name()}-{user_name}-job-cluster-role"
    cluster_role = client.V1ClusterRole(
        metadata=client.V1ObjectMeta(name=cluster_role_name),
        rules=[
            client.V1PolicyRule(
                api_groups=["keda.sh"],
                resources=["scaledjobs"],
                verbs=["create", "get", "list", "delete"]
            )
        ]
    )
    try:
        rbac_api.create_cluster_role(body=cluster_role)
    except ApiException as e:
        if e.status == 409:
            print(f"ClusterRole {cluster_role_name} already exists.")
        else:
            raise
    print(f"ClusterRole {cluster_role_name} created successfully.")
    group_name = f"{get_cluster_name()}-{user_name}-job-access"
    cluster_role_binding_name = f"{get_cluster_name()}-{user_name}-job-cluster-role-binding"
    # Define ClusterRoleBinding to bind the role to a user
    cluster_role_binding = client.V1ClusterRoleBinding(
        metadata=client.V1ObjectMeta(name=cluster_role_binding_name),
        role_ref=client.V1RoleRef(
            api_group="rbac.authorization.k8s.io",
            kind="ClusterRole",
            name=cluster_role_name
        ),
        subjects=[
            client.RbacV1Subject(
                kind="Group",
                name=group_name,
            )
        ]
    )
    try:
        rbac_api.create_cluster_role_binding(body=cluster_role_binding)
    except ApiException as e:
        if e.status == 409:
            print(f"ClusterRoleBinding {cluster_role_binding_name} already exists.")
        else:
            raise
    print(f"ClusterRoleBinding {cluster_role_binding_name} created successfully.")
    add_user_to_aws_auth_group(user_name, group_name)
    return



def generate_kubeconfig():
    eks_client = boto3.client(
        'eks',
        region_name=REGION,
    )

    cluster_name = get_cluster_name()
    # Retrieve cluster information
    cluster_info = eks_client.describe_cluster(name=get_cluster_name())['cluster']

    # Extract cluster details
    endpoint = cluster_info['endpoint']
    cluster_ca_certificate = cluster_info['certificateAuthority']['data']


    # Create a kubeconfig dictionary
    kubeconfig_data = {
        "apiVersion": "v1",
        "clusters": [{
            "cluster": {
                "server": endpoint,
                "certificate-authority-data": cluster_ca_certificate
            },
            "name": f'arn:aws:eks:us-east-1:{get_aws_account_id()}:cluster/{cluster_name}'
        }],
        "contexts": [{
            "context": {
                "cluster": f'arn:aws:eks:us-east-1:{get_aws_account_id()}:cluster/{cluster_name}',
                "user": f'arn:aws:eks:us-east-1:{get_aws_account_id()}:cluster/{cluster_name}'
            },
            "name": f'arn:aws:eks:us-east-1:{get_aws_account_id()}:cluster/{cluster_name}'
        }],
        "current-context": f'arn:aws:eks:us-east-1:{get_aws_account_id()}:cluster/{cluster_name}',
        "kind": "Config",
        "users": [{
            "name": f'arn:aws:eks:us-east-1:{get_aws_account_id()}:cluster/{cluster_name}',
            "user": {
                "exec": {
                    "apiVersion": "client.authentication.k8s.io/v1beta1",
                    "command": "aws",
                    "args": [
                        "eks",
                        "get-token",
                        "--cluster-name", cluster_name
                    ],
                    "env": [
                        {"name": "AWS_DEFAULT_REGION", "value": REGION}
                    ]
                }
            }
        }]
    }
    kubeconfig_dir = os.path.expanduser('~/.kube')
    kubeconfig_file = os.path.join(kubeconfig_dir, 'config')

    # Create the directory if it does not exist
    if not os.path.exists(kubeconfig_dir):
        os.makedirs(kubeconfig_dir,exist_ok=True)

    # Load existing kubeconfig or create a new one if it doesn't exist
    if os.path.exists(kubeconfig_file):
        with open(kubeconfig_file, 'r') as f:
            existing_config = yaml.safe_load(f) or {}
    else:
        existing_config = {'apiVersion': 'v1', 'kind': 'Config', 'clusters': [], 'contexts': [], 'users': []}

    # Merge new kubeconfig entry into existing config
    # Function to update or add an entry in the list
    def update_or_add_entry(existing_list, new_entry, key):
        for i, entry in enumerate(existing_list):
            if entry[key] == new_entry[key]:
                existing_list[i] = new_entry  # Update the existing entry
                return
        existing_list.append(new_entry)  # Add as a new entry if not found

    # Merge new kubeconfig entry into existing config
    update_or_add_entry(existing_config['clusters'], kubeconfig_data['clusters'][0], 'name')
    update_or_add_entry(existing_config['contexts'], kubeconfig_data['contexts'][0], 'name')
    update_or_add_entry(existing_config['users'], kubeconfig_data['users'][0], 'name')
    existing_config['current-context'] = kubeconfig_data['current-context']


    # Write back to the default kubeconfig file
    with open(kubeconfig_file, 'w') as f:
        yaml.dump(existing_config, f)

def create_service_account(name: str, namespace: str, context_name: Optional[str] = None):
    if not context_name:
        context_name = get_tensorkube_cluster_context_name()
        if not context_name:
            raise Exception("No context found for the cluster. Please configure Tensorfuse properly.")

    k8s_client = config.new_client_from_config(context=context_name)
    v1 = client.CoreV1Api(k8s_client)
    service_account = client.V1ServiceAccount()
    service_account.metadata = client.V1ObjectMeta(name=name)
    try:
        v1.create_namespaced_service_account(namespace=namespace, body=service_account)
    except ApiException as e:
        raise e
    

def create_service_account_with_role_arn(name: str, namespace: str, role_arn: str, context_name: Optional[str] = None):
    if not context_name:
        context_name = get_tensorkube_cluster_context_name()
        if not context_name:
            raise Exception("No context found for the cluster. Please configure Tensorfuse properly.")

    k8s_client = config.new_client_from_config(context=context_name)
    v1 = client.CoreV1Api(k8s_client)

    # Check if the ServiceAccount already exists
    try:
        v1.read_namespaced_service_account(name=name, namespace=namespace)
        print(f"ServiceAccount '{name}' already exists in namespace '{namespace}'.")
    except ApiException as e:
        if e.status == 404:
            # ServiceAccount does not exist; create it
            service_account = client.V1ServiceAccount(
                metadata=client.V1ObjectMeta(
                    name=name,
                    annotations={"eks.amazonaws.com/role-arn": role_arn},
                    namespace=namespace
                ),
            )
            try:
                v1.create_namespaced_service_account(namespace=namespace, body=service_account)
                print(f"ServiceAccount '{name}' created in namespace '{namespace}'.")
            except ApiException as create_error:
                print(f"Failed to create ServiceAccount '{name}': {create_error}")
                raise create_error
        else:
            print(f"Failed to check ServiceAccount existence: {e}")
            raise e



def create_k8s_role(role_name: str, namespace: str, rules: List[Dict[str, Any]], context_name: Optional[str] = None):
    if not context_name:
        context_name = get_tensorkube_cluster_context_name()
        if not context_name:
            raise Exception("No context found for the cluster. Please configure Tensorfuse properly.")

    k8s_client = config.new_client_from_config(context=context_name)
    rbac_api = client.RbacAuthorizationV1Api(k8s_client)
    role = client.V1Role()
    role.metadata = client.V1ObjectMeta(name=role_name)
    role.rules = rules
    try:
        rbac_api.create_namespaced_role(namespace=namespace, body=role)
    except ApiException as e:
        raise e

def create_role_binding(rb_name: str, rb_namespace: str, role_name: str, sa_name: str, sa_namespace: str, context_name: Optional[str] = None):
    if not context_name:
        context_name = get_tensorkube_cluster_context_name()
        if not context_name:
            raise Exception("No context found for the cluster. Please configure Tensorfuse properly.")

    k8s_api_client = config.new_client_from_config(context=context_name)
    rbac_api = client.RbacAuthorizationV1Api(k8s_api_client)
    role_binding = client.V1RoleBinding(
        role_ref=client.V1RoleRef(api_group="rbac.authorization.k8s.io", kind="Role", name=role_name),
        subjects=[client.RbacV1Subject(kind="ServiceAccount", name=sa_name, namespace=sa_namespace)])
    role_binding.metadata = client.V1ObjectMeta(name=rb_name)
    try:
        rbac_api.create_namespaced_role_binding(namespace=rb_namespace, body=role_binding)
    except ApiException as e:
        raise e


def is_existing_scaled_job(job_name: str, namespace: str, context_name: Optional[str] = None):
    k8s_api_client = config.new_client_from_config(context=context_name)
    k8s_client = client.CustomObjectsApi(k8s_api_client)
    try:
        job = k8s_client.get_namespaced_custom_object(
            group="keda.sh",
            version="v1alpha1",
            plural="scaledjobs",
            name=job_name,
            namespace=namespace
        )
        return True, job
    except ApiException as e:
        if e.status == 404:
            return False, None
        raise e
