import os
import platform
import subprocess

import click


def check_and_install_kubectl():
    """Check if kubectl is installed and install it if it's not."""
    try:
        subprocess.run(["kubectl", "version", "--client"], check=True)
        print("kubectl is already installed.")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("kubectl is not installed. Proceeding with installation.")
        if platform.system() == "Darwin":
            try:
                subprocess.run(["brew", "install", "kubectl"], check=True)
            except subprocess.CalledProcessError as e:
                print("Unable to install kubectl using Homebrew. Please install kubectl manually.")
                raise e
        elif platform.system() == "Linux":
            try:
                architecture = "arm64" if 'arm' in platform.machine() else "amd64"
                install_kubectl(architecture)
            except subprocess.CalledProcessError as e:
                print("Unable to install kubectl. Please install kubectl manually.")
                raise e
        else:
            print("Unsupported operating system. Please install kubectl manually.")
            raise Exception('Unsupported operating system.')

        # Verify kubectl installation
        try:
            subprocess.run(["kubectl", "version", "--client"], check=True)
            print("kubectl installed successfully.")
        except subprocess.CalledProcessError as e:
            print("kubectl installation failed. Please install kubectl manually.")
            raise e


def check_and_install_helm():
    """Check if helm is installed and install it if it's not."""
    try:
        subprocess.run(["helm", "version"], check=True)
        print("Helm is already installed.")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Helm is not installed. Proceeding with installation.")
        if platform.system() == "Darwin":
            try:
                subprocess.run(["brew", "install", "helm"], check=True)
            except subprocess.CalledProcessError as e:
                print("Unable to install helm using Homebrew. Please install helm manually.")
                raise e
        elif platform.system() == "Linux":
            print("Helm is not installed. Proceeding with installation.")
            try:
                install_helm_using_downloader()
            except Exception as e:
                click.echo(f"Error while installing helm: {e}. Please install helm manually", err=True)
                raise e
        else:
            print("Unsupported operating system. Please install helm manually.")
            raise Exception('Unsupported operating system.')

        # Verify helm installation
        try:
            subprocess.run(["helm", "version"], check=True)
            print("Helm installed successfully.")
        except subprocess.CalledProcessError as e:
            print("Helm installation failed. Please install helm manually.")
            raise e


def install_helm_using_downloader():
    try:
        # Download Helm installer script
        click.echo("Downloading Helm installer script...")
        subprocess.run(
            "curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3",
            shell=True,
            check=True
        )
        click.echo("Helm installer script downloaded successfully.")

        # Make the script executable
        click.echo("Making the script executable...")
        subprocess.run("chmod 700 get_helm.sh", shell=True, check=True)
        click.echo("Script made executable.")

        # Run the script to install Helm
        click.echo("Running the installer script...")
        subprocess.run("./get_helm.sh", shell=True, check=True)
        click.echo("Helm installed successfully.")

        # Delete the installer script
        click.echo("Deleting the installer script...")
        os.remove("get_helm.sh")
        click.echo("Installer script deleted successfully.")

        # Check Helm version
        click.echo("Checking Helm version...")
        subprocess.run("helm version", shell=True, check=True)
        click.echo("Helm installation and verification completed successfully.")

    except subprocess.CalledProcessError as e:
        click.echo(f"An error occurred: {e}", err=True)
        raise e
    except OSError as e:
        click.echo(f"Error deleting the installer script: {e}", err=True)


def install_kubectl(architecture):
    valid_architectures = {"amd64", "arm64"}
    if architecture not in valid_architectures:
        click.echo(f"Invalid architecture: {architecture}. Valid options are: {valid_architectures}", err=True)
        return

    try:
        # Download kubectl binary for the specified architecture
        click.echo(f"Downloading kubectl binary for {architecture} architecture...")
        subprocess.run(
            f"curl -LO https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/{architecture}/kubectl",
            shell=True,
            check=True
        )
        click.echo(f"kubectl binary for {architecture} downloaded successfully.")

        # Download kubectl sha256 checksum for the specified architecture
        click.echo(f"Downloading kubectl sha256 checksum for {architecture} architecture...")
        subprocess.run(
            f"curl -LO https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/{architecture}/kubectl.sha256",
            shell=True,
            check=True
        )
        click.echo(f"kubectl sha256 checksum for {architecture} downloaded successfully.")

        # Verify the sha256 checksum
        click.echo(f"Verifying the downloaded binary for {architecture} architecture...")
        subprocess.run(
            f"echo \"$(cat kubectl.sha256)  kubectl\" | sha256sum --check",
            shell=True,
            check=True
        )
        click.echo("Verification successful.")

        # Install kubectl
        click.echo(f"Installing kubectl for {architecture} architecture...")
        subprocess.run(
            "sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl",
            shell=True,
            check=True
        )
        click.echo(f"kubectl for {architecture} installed successfully.")

        # Check kubectl version
        click.echo("Checking kubectl version...")
        subprocess.run(
            "kubectl version --client",
            shell=True,
            check=True
        )
        click.echo(f"kubectl installation and verification for {architecture} completed successfully.")

    except subprocess.CalledProcessError as e:
        click.echo(f"An error occurred: {e}", err=True)