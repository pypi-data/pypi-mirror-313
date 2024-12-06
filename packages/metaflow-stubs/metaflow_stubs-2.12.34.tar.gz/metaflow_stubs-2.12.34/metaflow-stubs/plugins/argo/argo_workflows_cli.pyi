######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.12.34                                                                                #
# Generated on 2024-12-04T14:12:34.694604                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.exception

from ...parameters import JSONType as JSONType
from ...client.core import Run as Run
from ...metaflow_current import current as current
from ... import parameters as parameters
from ..._vendor import click as click
from ...client.core import get_metadata as get_metadata
from ...exception import MetaflowException as MetaflowException
from ...exception import MetaflowInternalError as MetaflowInternalError
from ...exception import MetaflowNotFound as MetaflowNotFound
from ..aws.step_functions.production_token import load_token as load_token
from ..aws.step_functions.production_token import new_token as new_token
from ..aws.step_functions.production_token import store_token as store_token
from ..environment_decorator import EnvironmentDecorator as EnvironmentDecorator
from ..kubernetes.kubernetes_decorator import KubernetesDecorator as KubernetesDecorator
from ...tagging_util import validate_tags as validate_tags
from .argo_workflows import ArgoWorkflows as ArgoWorkflows

ARGO_WORKFLOWS_UI_URL: None

KUBERNETES_NAMESPACE: str

SERVICE_VERSION_CHECK: bool

UI_URL: None

unsupported_decorators: dict

class IncorrectProductionToken(metaflow.exception.MetaflowException, metaclass=type):
    ...

class RunIdMismatch(metaflow.exception.MetaflowException, metaclass=type):
    ...

class IncorrectMetadataServiceVersion(metaflow.exception.MetaflowException, metaclass=type):
    ...

class ArgoWorkflowsNameTooLong(metaflow.exception.MetaflowException, metaclass=type):
    ...

class UnsupportedPythonVersion(metaflow.exception.MetaflowException, metaclass=type):
    ...

def check_python_version(obj):
    ...

def check_metadata_service_version(obj):
    ...

def resolve_workflow_name(obj, name):
    ...

def make_flow(obj, token, name, tags, namespace, max_workers, workflow_timeout, workflow_priority, auto_emit_argo_events, notify_on_error, notify_on_success, notify_slack_webhook_url, notify_pager_duty_integration_key, enable_heartbeat_daemon, enable_error_msg_capture):
    ...

def resolve_token(name, token_prefix, obj, authorize, given_token, generate_new_token, is_project):
    ...

def validate_token(name, token_prefix, authorize, instructions_fn = None):
    """
    Validate that the production token matches that of the deployed flow.
    In case both the user and token do not match, raises an error.
    Optionally outputs instructions on token usage via the provided instruction_fn(flow_name, prev_user)
    """
    ...

def get_run_object(pathspec: str):
    ...

def get_status_considering_run_object(status, run_obj):
    ...

def validate_run_id(workflow_name, token_prefix, authorize, run_id, instructions_fn = None):
    """
    Validates that a run_id adheres to the Argo Workflows naming rules, and
    that it belongs to the current flow (accounting for project branch as well).
    """
    ...

def sanitize_for_argo(text):
    """
    Sanitizes a string so it does not contain characters that are not permitted in Argo Workflow resource names.
    """
    ...

def remap_status(status):
    """
    Group similar Argo Workflow statuses together in order to have similar output to step functions statuses.
    """
    ...

