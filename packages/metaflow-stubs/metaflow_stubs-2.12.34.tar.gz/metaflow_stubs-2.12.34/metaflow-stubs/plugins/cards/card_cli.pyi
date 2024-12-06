######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.12.34                                                                                #
# Generated on 2024-12-04T14:12:34.671998                                                            #
######################################################################################################

from __future__ import annotations


from ...client.core import Task as Task
from ...parameters import JSONTypeClass as JSONTypeClass
from ...client.core import namespace as namespace
from ...exception import CommandException as CommandException
from ...exception import MetaflowNotFound as MetaflowNotFound
from ...exception import MetaflowNamespaceMismatch as MetaflowNamespaceMismatch
from ..._vendor import click as click
from .card_datastore import CardDatastore as CardDatastore
from .exception import CardClassFoundException as CardClassFoundException
from .exception import IncorrectCardArgsException as IncorrectCardArgsException
from .exception import UnrenderableCardException as UnrenderableCardException
from .exception import CardNotPresentException as CardNotPresentException
from .exception import TaskNotFoundException as TaskNotFoundException
from .card_resolver import resolve_paths_from_task as resolve_paths_from_task
from .card_resolver import resumed_info as resumed_info

NUM_SHORT_HASH_CHARS: int

class CardRenderInfo(tuple, metaclass=type):
    """
    CardRenderInfo(mode, is_implemented, data, timed_out, timeout_stack_trace)
    """
    @staticmethod
    def __new__(_cls, mode, is_implemented, data, timed_out, timeout_stack_trace):
        """
        Create new instance of CardRenderInfo(mode, is_implemented, data, timed_out, timeout_stack_trace)
        """
        ...
    def __repr__(self):
        """
        Return a nicely formatted representation string
        """
        ...
    def __getnewargs__(self):
        """
        Return self as a plain tuple.  Used by copy and pickle.
        """
        ...
    ...

def open_in_browser(card_path):
    ...

def resolve_task_from_pathspec(flow_name, pathspec):
    """
    resolves a task object for the pathspec query on the CLI.
    Args:
        flow_name : (str) : name of flow
        pathspec (str) : can be `stepname` / `runid/stepname` / `runid/stepname/taskid`
    
    Returns:
        metaflow.Task | None
    """
    ...

def resolve_card(ctx, pathspec, follow_resumed = True, hash = None, type = None, card_id = None, no_echo = False):
    """
    Resolves the card path for a query.
    
    Args:
        ctx: click context object
        pathspec: pathspec can be `stepname` or `runid/stepname` or `runid/stepname/taskid`
        hash (optional): This is to specifically resolve the card via the hash. This is useful when there may be many card with same id or type for a pathspec.
        type : type of card
        card_id : `id` given to card
        no_echo : if set to `True` then supress logs about pathspec resolution.
    Raises:
        CardNotPresentException: No card could be found for the pathspec
    
    Returns:
        (card_paths, card_datastore, taskpathspec) : Tuple[List[str], CardDatastore, str]
    """
    ...

def timeout(time):
    ...

def raise_timeout(signum, frame):
    ...

def list_available_cards(ctx, pathspec, card_paths, card_datastore, command = 'view', show_list_as_json = False, list_many = False, file = None):
    ...

def make_command(script_name, taskspec, command = 'get', hash = None):
    ...

def list_many_cards(ctx, type = None, hash = None, card_id = None, follow_resumed = None, as_json = None, file = None):
    ...

def card_read_options_and_arguments(func):
    ...

def update_card(mf_card, mode, task, data, timeout_value = None):
    """
    This method will be responsible for creating a card/data-update based on the `mode`.
    There are three possible modes taken by this function.
        - render :
            - This will render the "final" card.
            - This mode is passed at task completion.
            - Setting this mode will call the `render` method of a MetaflowCard.
            - It will result in the creation of an HTML page.
        - render_runtime:
            - Setting this mode will render a card during task "runtime".
            - Setting this mode will call the `render_runtime` method of a MetaflowCard.
            - It will result in the creation of an HTML page.
        - refresh:
            - Setting this mode will refresh the data update for a card.
            - We support this mode because rendering a full card can be an expensive operation, but shipping tiny data updates can be cheap.
            - Setting this mode will call the `refresh` method of a MetaflowCard.
            - It will result in the creation of a JSON object.
    
    Parameters
    ----------
    mf_card : MetaflowCard
        MetaflowCard object which will be used to render the card.
    mode : str
        Mode of rendering the card.
    task : Task
        Task object which will be passed to render the card.
    data : dict
        object created and passed down from `current.card._get_latest_data` method.
        For more information on this object's schema have a look at `current.card._get_latest_data` method.
    timeout_value : int
        Timeout value for rendering the card.
    
    Returns
    -------
    CardRenderInfo
        - NamedTuple which will contain:
            - `mode`: The mode of rendering the card.
            - `is_implemented`: whether the function was implemented or not.
            - `data` : output from rendering the card (Can be string/dict)
            - `timed_out` : whether the function timed out or not.
            - `timeout_stack_trace` : stack trace of the function if it timed out.
    """
    ...

