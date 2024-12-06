from tensorkube.services.eksctl_service import check_and_install_eksctl
from tensorkube.services.istio import check_and_install_istioctl
from tensorkube.services.kubectl_utils import check_and_install_kubectl, check_and_install_helm


def check_and_install_cli_tools():
    # check and install eksctl
    check_and_install_eksctl()
    # check if kubectl is present and if not install
    check_and_install_kubectl()
    # check and install istioctl
    check_and_install_istioctl()
    # check and install helm
    check_and_install_helm()