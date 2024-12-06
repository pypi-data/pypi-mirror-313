import os
import platform
import subprocess
from string import Template

from pkg_resources import resource_filename

from tensorkube.services.aws_service import get_aws_account_id, get_karpenter_namespace
from tensorkube.constants import get_cluster_name


# create base cluster using eksctl

def create_base_tensorkube_cluster_eksctl(cluster_name):
    yaml_file_path = resource_filename('tensorkube', 'configurations/base_cluster.yaml')
    # variables
    variables = {"CLUSTER_NAME": cluster_name, "AWS_DEFAULT_REGION": "us-east-1", "K8S_VERSION": "1.29",
                 "AWS_ACCOUNT_ID": get_aws_account_id(), "KARPENTER_NAMESPACE": get_karpenter_namespace(),
                 "AWS_PARTITION": "aws", }

    with open(yaml_file_path) as file:
        template = file.read()
    yaml_content = Template(template).substitute(variables)

    temp_yaml_file_path = "/tmp/temp_cluster.yaml"
    with open(temp_yaml_file_path, 'w') as file:
        file.write(yaml_content)

    # Check if the cluster already exists
    try:
        subprocess.run(["eksctl", "get", "cluster", cluster_name], check=True)
        print(f'Cluster {cluster_name} already exists.')
        os.remove(temp_yaml_file_path)
        return None
    except subprocess.CalledProcessError:
        pass  # Cluster does not exist, we can create it

        # Run the eksctl create cluster command
    command = ["eksctl", "create", "cluster", "-f", temp_yaml_file_path]
    subprocess.run(command, check=True)

    # Remove the temporary file
    os.remove(temp_yaml_file_path)


def delete_cluster():
    command = ["eksctl", "delete", "cluster", "--name", get_cluster_name()]
    subprocess.run(command)


def check_and_install_eksctl():
    """Check if eksctl is installed and if not isntall it."""
    try:
        subprocess.run(["eksctl", "version"], check=True)
    except Exception as e:
        # check if the operating system is mac and install eksctl
        if platform.system() == "Darwin":
            try:
                subprocess.run(["brew", "install", "eksctl"])
            except Exception as mac_e:
                print("Unable to install eksctl. Please install eksctl manually.")
                raise mac_e
        elif platform.system() == "Linux":
            try:
                # curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
                # sudo mv /tmp/eksctl /usr/local/bin
                # eksctl version
                download_command = [
                    "curl", "--silent", "--location",
                    "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz",
                    "-o", "/tmp/eksctl.tar.gz"
                ]
                subprocess.run(" ".join(download_command), shell=True, check=True)
                # Extract the tar.gz file
                extract_command = ["tar", "xzf", "/tmp/eksctl.tar.gz", "-C", "/tmp"]
                subprocess.run(extract_command, check=True)
                # Move the binary to /usr/local/bin
                move_command = ["sudo", "mv", "/tmp/eksctl", "/usr/local/bin"]
                subprocess.run(move_command, check=True)
                subprocess.run(["eksctl", "version"])
            except Exception as linux_e:
                print("Unable to install eksctl. Please install eksctl manually.")
                raise linux_e
        else:
            print("eksctl is not installed. Please install eksctl manually.")
            raise e


def delete_nodegroup(nodegroup_name):
    # Construct the eksctl command to delete the nodegroup
    delete_command = f"eksctl delete nodegroup --name={nodegroup_name} --cluster={get_cluster_name()} --wait"

    # Execute the command
    print(f"Initiating deletion of nodegroup {nodegroup_name}...")
    subprocess.run(delete_command, shell=True, check=True)
    print(f"Nodegroup {nodegroup_name} deletion initiated. Please wait for the process to complete.")
