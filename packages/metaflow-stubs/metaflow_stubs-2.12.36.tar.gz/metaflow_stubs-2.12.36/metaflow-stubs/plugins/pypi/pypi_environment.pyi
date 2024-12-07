######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.12.36                                                                                #
# Generated on 2024-12-07T00:02:15.879997                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.plugins.pypi.conda_environment

from .conda_environment import CondaEnvironment as CondaEnvironment

class PyPIEnvironment(metaflow.plugins.pypi.conda_environment.CondaEnvironment, metaclass=type):
    ...

