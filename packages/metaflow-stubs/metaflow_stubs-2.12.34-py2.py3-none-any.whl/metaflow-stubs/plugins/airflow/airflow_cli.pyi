######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.12.34                                                                                #
# Generated on 2024-12-04T14:12:34.676461                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.exception

from ...metaflow_current import current as current
from ..._vendor import click as click
from ...exception import MetaflowException as MetaflowException
from ...exception import MetaflowInternalError as MetaflowInternalError
from ..aws.step_functions.production_token import load_token as load_token
from ..aws.step_functions.production_token import new_token as new_token
from ..aws.step_functions.production_token import store_token as store_token
from ..kubernetes.kubernetes_decorator import KubernetesDecorator as KubernetesDecorator
from .airflow import Airflow as Airflow
from .exception import AirflowException as AirflowException
from .exception import NotSupportedException as NotSupportedException

class IncorrectProductionToken(metaflow.exception.MetaflowException, metaclass=type):
    ...

def resolve_token(name, token_prefix, obj, authorize, given_token, generate_new_token, is_project):
    ...

def make_flow(obj, dag_name, production_token, tags, is_paused_upon_creation, namespace, max_workers, workflow_timeout, worker_pool, file):
    ...

def resolve_dag_name(name):
    ...

