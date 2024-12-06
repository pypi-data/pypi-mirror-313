######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.12.34                                                                                #
# Generated on 2024-12-04T14:12:34.654644                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.decorators

from ..exception import MetaflowException as MetaflowException
from ..metaflow_current import current as current

VALID_NAME_RE: str

VALID_NAME_LEN: int

class ProjectDecorator(metaflow.decorators.FlowDecorator, metaclass=type):
    """
    Specifies what flows belong to the same project.
    
    A project-specific namespace is created for all flows that
    use the same `@project(name)`.
    
    Parameters
    ----------
    name : str
        Project name. Make sure that the name is unique amongst all
        projects that use the same production scheduler. The name may
        contain only lowercase alphanumeric characters and underscores.
    
    MF Add To Current
    -----------------
    project_name -> str
        The name of the project assigned to this flow, i.e. `X` in `@project(name=X)`.
    
        @@ Returns
        -------
        str
            Project name.
    
    project_flow_name -> str
        The flow name prefixed with the current project and branch. This name identifies
        the deployment on a production scheduler.
    
        @@ Returns
        -------
        str
            Flow name prefixed with project information.
    
    branch_name -> str
        The current branch, i.e. `X` in `--branch=X` set during deployment or run.
    
        @@ Returns
        -------
        str
            Branch name.
    
    is_user_branch -> bool
        True if the flow is deployed without a specific `--branch` or a `--production`
        flag.
    
        @@ Returns
        -------
        bool
            True if the deployment does not correspond to a specific branch.
    
    is_production -> bool
        True if the flow is deployed with the `--production` flag
    
        @@ Returns
        -------
        bool
            True if the flow is deployed with `--production`.
    """
    def flow_init(self, flow, graph, environment, flow_datastore, metadata, logger, echo, options):
        ...
    def get_top_level_options(self):
        ...
    ...

def format_name(flow_name, project_name, deploy_prod, given_branch, user_name):
    ...

