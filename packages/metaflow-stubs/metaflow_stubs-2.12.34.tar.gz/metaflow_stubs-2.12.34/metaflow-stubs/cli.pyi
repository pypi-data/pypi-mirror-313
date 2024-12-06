######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.12.34                                                                                #
# Generated on 2024-12-04T14:12:34.643547                                                            #
######################################################################################################

from __future__ import annotations


from ._vendor import click as click
from .client.core import get_metadata as get_metadata
from .client.core import namespace as namespace
from . import parameters as parameters
from . import plugins as plugins
from .exception import CommandException as CommandException
from .exception import MetaflowException as MetaflowException
from .metaflow_current import current as current
from .mflog import mflog as mflog
from .pylint_wrapper import PyLint as PyLint
from .tagging_util import validate_tags as validate_tags

DECOSPECS: str

DEFAULT_DATASTORE: str

DEFAULT_ENVIRONMENT: str

DEFAULT_EVENT_LOGGER: str

DEFAULT_METADATA: str

DEFAULT_MONITOR: str

DEFAULT_PACKAGE_SUFFIXES: str

LOG_SOURCES: list

DATASTORES: list

ENVIRONMENTS: list

LOGGING_SIDECARS: dict

METADATA_PROVIDERS: list

MONITOR_SIDECARS: dict

UBF_CONTROL: str

UBF_TASK: str

ERASE_TO_EOL: str

HIGHLIGHT: str

INDENT: str

LOGGER_TIMESTAMP: str

LOGGER_COLOR: str

LOGGER_BAD_COLOR: str

def echo_dev_null(*args, **kwargs):
    ...

def echo_always(line, **kwargs):
    ...

def logger(body = '', system_msg = False, head = '', bad = False, timestamp = True, nl = True):
    ...

def config_merge_cb(ctx, param, value):
    ...

def common_run_options(func):
    ...

def write_file(file_path, content):
    ...

def before_run(obj, tags, decospecs):
    ...

def print_metaflow_exception(ex):
    ...

def print_unknown_exception(ex):
    ...

class CliState(object, metaclass=type):
    def __init__(self, flow):
        ...
    ...

def main(flow, args = None, handle_exceptions = True, entrypoint = None):
    ...

