######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.12.34                                                                                #
# Generated on 2024-12-04T14:12:34.628232                                                            #
######################################################################################################

from __future__ import annotations


from . import test_unbounded_foreach_decorator as test_unbounded_foreach_decorator
from .test_unbounded_foreach_decorator import InternalTestUnboundedForeachInput as InternalTestUnboundedForeachInput
from . import parallel_decorator as parallel_decorator
from . import environment_decorator as environment_decorator
from . import retry_decorator as retry_decorator
from . import catch_decorator as catch_decorator
from . import cards as cards
from . import frameworks as frameworks
from . import secrets as secrets
from . import airflow as airflow
from . import aws as aws
from . import resources_decorator as resources_decorator
from . import timeout_decorator as timeout_decorator
from . import datatools as datatools
from . import kubernetes as kubernetes
from . import pypi as pypi
from . import argo as argo
from . import events_decorator as events_decorator
from . import project_decorator as project_decorator
from . import azure as azure
from . import storage_executor as storage_executor
from . import gcp as gcp
from . import debug_logger as debug_logger
from . import debug_monitor as debug_monitor
from .cards.card_modules.basic import BlankCard as BlankCard
from .cards.card_modules.basic import DefaultCard as DefaultCard
from .cards.card_modules.basic import DefaultCardJSON as DefaultCardJSON
from .cards.card_modules.basic import ErrorCard as ErrorCard
from .cards.card_modules.basic import TaskSpecCard as TaskSpecCard
from .cards.card_modules.test_cards import TestEditableCard as TestEditableCard
from .cards.card_modules.test_cards import TestEditableCard2 as TestEditableCard2
from .cards.card_modules.test_cards import TestErrorCard as TestErrorCard
from .cards.card_modules.test_cards import TestMockCard as TestMockCard
from .cards.card_modules.test_cards import TestNonEditableCard as TestNonEditableCard
from .cards.card_modules.test_cards import TestPathSpecCard as TestPathSpecCard
from .cards.card_modules.test_cards import TestTimeoutCard as TestTimeoutCard
from .cards.card_modules.test_cards import TestRefreshCard as TestRefreshCard
from .cards.card_modules.test_cards import TestRefreshComponentCard as TestRefreshComponentCard
from . import tag_cli as tag_cli
from . import logs_cli as logs_cli
from . import package_cli as package_cli

CLIS_DESC: list

STEP_DECORATORS_DESC: list

FLOW_DECORATORS_DESC: list

ENVIRONMENTS_DESC: list

METADATA_PROVIDERS_DESC: list

DATASTORES_DESC: list

DATACLIENTS_DESC: list

SIDECARS_DESC: list

LOGGING_SIDECARS_DESC: list

MONITOR_SIDECARS_DESC: list

AWS_CLIENT_PROVIDERS_DESC: list

SENSOR_FLOW_DECORATORS: list

SECRETS_PROVIDERS_DESC: list

GCP_CLIENT_PROVIDERS_DESC: list

AZURE_CLIENT_PROVIDERS_DESC: list

DEPLOYER_IMPL_PROVIDERS_DESC: list

def get_plugin_cli():
    ...

STEP_DECORATORS: list

FLOW_DECORATORS: list

ENVIRONMENTS: list

METADATA_PROVIDERS: list

DATASTORES: list

DATACLIENTS: list

SIDECARS: dict

LOGGING_SIDECARS: dict

MONITOR_SIDECARS: dict

AWS_CLIENT_PROVIDERS: list

SECRETS_PROVIDERS: list

AZURE_CLIENT_PROVIDERS: list

GCP_CLIENT_PROVIDERS: list

DEPLOYER_IMPL_PROVIDERS: list

MF_EXTERNAL_CARDS: list

CARDS: list

