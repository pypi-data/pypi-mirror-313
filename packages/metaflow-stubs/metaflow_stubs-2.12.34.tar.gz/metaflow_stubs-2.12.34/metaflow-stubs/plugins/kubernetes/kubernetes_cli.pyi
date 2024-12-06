######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.12.34                                                                                #
# Generated on 2024-12-04T14:12:34.684329                                                            #
######################################################################################################

from __future__ import annotations


from .kube_utils import parse_cli_options as parse_cli_options
from .kubernetes_client import KubernetesClient as KubernetesClient
from ...parameters import JSONTypeClass as JSONTypeClass
from ..._vendor import click as click
from ...exception import MetaflowException as MetaflowException
from ...metadata_provider.util import sync_local_metadata_from_datastore as sync_local_metadata_from_datastore
from .kubernetes import Kubernetes as Kubernetes
from .kubernetes import KubernetesException as KubernetesException
from .kubernetes import KubernetesKilledException as KubernetesKilledException
from .kubernetes import parse_kube_keyvalue_list as parse_kube_keyvalue_list
from .kubernetes_decorator import KubernetesDecorator as KubernetesDecorator

METAFLOW_EXIT_DISALLOW_RETRY: int

DATASTORE_LOCAL_DIR: str

KUBERNETES_LABELS: str

TASK_LOG_SOURCE: str

UBF_CONTROL: str

UBF_TASK: str

