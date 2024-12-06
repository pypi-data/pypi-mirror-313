######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.12.34                                                                                #
# Generated on 2024-12-04T14:12:34.676012                                                            #
######################################################################################################

from __future__ import annotations


from ...metaflow_current import current as current
from ...exception import MetaflowException as MetaflowException
from ...includefile import FilePathClass as FilePathClass
from ...parameters import DelayedEvaluationParameter as DelayedEvaluationParameter
from ...parameters import JSONTypeClass as JSONTypeClass
from ...parameters import deploy_time_eval as deploy_time_eval
from ..cards.card_modules import chevron as chevron
from ..kubernetes.kubernetes import Kubernetes as Kubernetes
from ..timeout_decorator import get_run_time_limit_for_task as get_run_time_limit_for_task
from . import airflow_utils as airflow_utils
from .airflow_utils import AIRFLOW_MACROS as AIRFLOW_MACROS
from .airflow_utils import AirflowTask as AirflowTask
from .airflow_utils import Workflow as Workflow
from .exception import AirflowException as AirflowException

AIRFLOW_KUBERNETES_CONN_ID: None

AIRFLOW_KUBERNETES_KUBECONFIG_CONTEXT: None

AIRFLOW_KUBERNETES_KUBECONFIG_FILE: None

AIRFLOW_KUBERNETES_STARTUP_TIMEOUT_SECONDS: int

AWS_SECRETS_MANAGER_DEFAULT_REGION: None

GCP_SECRET_MANAGER_PREFIX: None

AZURE_STORAGE_BLOB_SERVICE_ENDPOINT: None

CARD_AZUREROOT: None

CARD_GSROOT: None

CARD_S3ROOT: None

DATASTORE_SYSROOT_AZURE: None

DATASTORE_SYSROOT_GS: None

DATASTORE_SYSROOT_S3: None

DATATOOLS_S3ROOT: None

DEFAULT_SECRETS_BACKEND_TYPE: None

KUBERNETES_SECRETS: str

KUBERNETES_SERVICE_ACCOUNT: None

S3_ENDPOINT_URL: None

SERVICE_HEADERS: dict

SERVICE_INTERNAL_URL: None

AZURE_KEY_VAULT_PREFIX: None

TASK_ID_XCOM_KEY: str

SUPPORTED_SENSORS: list

AIRFLOW_DEPLOY_TEMPLATE_FILE: str

class Airflow(object, metaclass=type):
    def __init__(self, name, graph, flow, code_package_sha, code_package_url, metadata, flow_datastore, environment, event_logger, monitor, production_token, tags = None, namespace = None, username = None, max_workers = None, worker_pool = None, description = None, file_path = None, workflow_timeout = None, is_paused_upon_creation = True):
        ...
    @classmethod
    def get_existing_deployment(cls, name, flow_datastore):
        ...
    @classmethod
    def get_token_path(cls, name):
        ...
    @classmethod
    def save_deployment_token(cls, owner, name, token, flow_datastore):
        ...
    def compile(self):
        ...
    ...

