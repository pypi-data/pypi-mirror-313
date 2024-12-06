from enum import Enum
from typing import Optional
import os

REGION = 'us-east-1'
NAMESPACE = 'kube-system'
DEFAULT_NAMESPACE = 'default'
SERVICE_ACCOUNT_NAME = 's3-csi-driver-sa'
ADDON_NAME = "aws-mountpoint-s3-csi-driver"
KNATIVE_SERVING_NAMESPACE = 'knative-serving'
CONFIG_FEATURES = 'config-features'
BUILD_TOOL = 'buildkit'
DATASET_BUCKET_TYPE = 'datasets'

KEDA_NAMESPACE = 'keda'
KEDA_SERVICE_ACCOUNT_NAME = 'keda-operator'
KEDA_IAM_ROLE_NAME = 'keda-iam-role'

TENSORFUSE_NAMESPACES = ['amazon-cloudwatch', 'kube-system', 'istio-system', 'knative-serving', 'kube-node-lease',
    'kube-public', 'kube-system', ]


def get_cluster_name():
    return "tensorkube"


def get_mount_policy_name(cluster_name:str, env: Optional[str] = None) -> str:
    if env:
        return f'{cluster_name}-mountpoint-policy-env-{env}'
    return f'{cluster_name}-mountpoint-policy'


def get_mount_driver_role_name(cluster_name):
    return f'{cluster_name}-mountpoint-driver-role'


class Events(Enum):
    CONFIGURE_START = 'configure-start'
    CONFIGURE_END = 'configure-end'
    CONFIGURE_ERROR = 'configure-error'

    DEPLOY_START = 'deploy-start'
    DEPLOY_END = 'deploy-end'
    DEPLOY_ERROR = 'deploy-error'

    DEVCONTAINER = 'devcontainer'
    DEVCONTAINER_START = 'devcontainer-start'
    DEVCONTAINER_STOP = 'devcontainer-stop'
    DEVCONTAINER_LIST = 'devcontainer-list'
    DEVCONTAINER_ERROR = 'devcontainer-error'

    JOB_DEPLOY_START = 'job-deploy-start'
    JOB_DEPLOY_END = 'job-deploy-end'
    JOB_DEPLOY_ERROR = 'job-deploy-error'

    TEST_START = 'test-start'
    TEST_END = 'test-end'


class PodStatus(Enum):
    PENDING = 'Pending'
    RUNNING = 'Running'
    SUCCEEDED = 'Succeeded'
    FAILED = 'Failed'
    UNKNOWN = 'Unknown'


class CliColors(Enum):
    ERROR = 'red'
    SUCCESS = 'green'
    WARNING = 'yellow'
    INFO = 'blue'
    DEFAULT = 'white'


def get_efs_service_account_name() -> str:
    return f'{get_cluster_name()}-efs-csi-controller-sa'


def get_efs_role_name() -> str:
    return f'AmazonEKS_EFS_CSI_DriverRole_{get_cluster_name()}'


def get_logging_service_account_name() -> str:
    return f'cloudwatch-agent'


def get_cloudwatch_role_name() -> str:
    return f'cloudwatch-agent-role_{get_cluster_name()}'


def get_cloudwatch_namespace() -> str:
    return 'amazon-cloudwatch'


def get_efs_security_group_name(env: Optional[str] = None) -> str:
    if env:
        return f'eks-efs-sg-{get_cluster_name()}-env-{env}'
    return f'eks-efs-sg-{get_cluster_name()}'


def get_base_login_url():
    return 'https://api.tensorfuse.io'
