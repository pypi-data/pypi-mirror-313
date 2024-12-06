######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.12.34                                                                                #
# Generated on 2024-12-04T14:12:34.708216                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.exception

from ....parameters import JSONType as JSONType
from ....metaflow_current import current as current
from .... import parameters as parameters
from ....client.core import get_metadata as get_metadata
from ...._vendor import click as click
from ....exception import MetaflowException as MetaflowException
from ....exception import MetaflowInternalError as MetaflowInternalError
from ..batch.batch_decorator import BatchDecorator as BatchDecorator
from ....tagging_util import validate_tags as validate_tags
from .production_token import load_token as load_token
from .production_token import new_token as new_token
from .production_token import store_token as store_token
from .step_functions import StepFunctions as StepFunctions

SERVICE_VERSION_CHECK: bool

SFN_STATE_MACHINE_PREFIX: None

UI_URL: None

class IncorrectProductionToken(metaflow.exception.MetaflowException, metaclass=type):
    ...

class RunIdMismatch(metaflow.exception.MetaflowException, metaclass=type):
    ...

class IncorrectMetadataServiceVersion(metaflow.exception.MetaflowException, metaclass=type):
    ...

class StepFunctionsStateMachineNameTooLong(metaflow.exception.MetaflowException, metaclass=type):
    ...

def check_metadata_service_version(obj):
    ...

def resolve_state_machine_name(obj, name):
    ...

def make_flow(obj, token, name, tags, namespace, max_workers, workflow_timeout, is_project, use_distributed_map):
    ...

def resolve_token(name, token_prefix, obj, authorize, given_token, generate_new_token, is_project):
    ...

def validate_run_id(state_machine_name, token_prefix, authorize, run_id, instructions_fn = None):
    ...

def validate_token(name, token_prefix, authorize, instruction_fn = None):
    """
    Validate that the production token matches that of the deployed flow.
    
    In case both the user and token do not match, raises an error.
    Optionally outputs instructions on token usage via the provided instruction_fn(flow_name, prev_user)
    """
    ...

