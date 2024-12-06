import platform
import subprocess
import os
import click

from tensorkube.configurations.configuration_urls import DOMAIN_SERVER_URL, KNATIVE_ISTIO_CONTROLLER_URL
from tensorkube.services.eks_service import get_pods_using_namespace, apply_yaml_from_url, delete_resources_from_url


def check_and_install_istioctl():
    """Check if istioctl is installed and install it if it's not."""
    try:
        subprocess.run(["istioctl", "version"], check=True)
        print("istioctl is already installed.")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("istioctl is not installed. Proceeding with installation.")
        if platform.system() == "Darwin":
            try:
                subprocess.run(["brew", "install", "istioctl"], check=True)
            except subprocess.CalledProcessError as e:
                print("Unable to install istioctl using Homebrew. Please install istioctl manually.")
                raise e
        elif platform.system() == "Linux":
            try:
                install_command = "curl -sL https://istio.io/downloadIstioctl | sh -"
                # Download and install istioctl
                subprocess.run(install_command, shell=True,
                               check=True)

                # Add istioctl to PATH
                istioctl_path = os.path.expanduser("~/.istioctl/bin")
                if istioctl_path not in os.environ["PATH"]:
                    os.environ["PATH"] += os.pathsep + istioctl_path
                    # Optionally, you can add this path to .bashrc or .bash_profile to make it permanent
                    with open(os.path.expanduser("~/.bashrc"), "a") as bashrc:
                        bashrc.write(f'\nexport PATH="$HOME/.istioctl/bin:$PATH"\n')

                print("istioctl installed successfully and PATH updated.")
            except subprocess.CalledProcessError as e:
                print("Unable to install istioctl using curl. Please install istioctl manually.")
                raise e
        else:
            print("Unsupported operating system. Please install istioctl manually.")
            raise Exception('Unsupported operating system.')

        # Verify istioctl installation
        try:
            subprocess.run(["istioctl", "version"], check=True)
            print("istioctl installed successfully.")
        except subprocess.CalledProcessError as e:
            print("istioctl installation failed. Please install istioctl manually.")
            raise e


def install_istio_on_cluster():
    """Install Istio with the default profile."""
    try:
        subprocess.run(["istioctl", "install", "--set", "profile=default", "-y"])
        print("Istio installed successfully.")
    except Exception as e:
        print(f"Error installing Istio: {e}")
        raise e
    # finally using the kubeconfi
    pods = get_pods_using_namespace("istio-system")
    for pod in pods.items:
        click.echo(f"Pod name: {pod.metadata.name}, Pod status: {pod.status.phase}")


def remove_domain_server():
    delete_resources_from_url(DOMAIN_SERVER_URL, "removing Knative Default Domain")


def uninstall_istio_from_cluster():
    """Uninstall Istio from the cluster."""
    # remove knative istion controller
    delete_resources_from_url(KNATIVE_ISTIO_CONTROLLER_URL, "uninstalling Knative Net Istio")
    # remove istio
    try:
        subprocess.run(["istioctl", "x", "uninstall", "--purge", "-y"])
        click.echo("Istio uninstalled successfully.")
    except Exception as e:
        click.echo(f"Error uninstalling Istio: {e}")


def install_net_istio():
    apply_yaml_from_url(KNATIVE_ISTIO_CONTROLLER_URL, "installing Knative Net Istio")


def install_default_domain():
    apply_yaml_from_url(DOMAIN_SERVER_URL, "installing Knative Default Domain")
