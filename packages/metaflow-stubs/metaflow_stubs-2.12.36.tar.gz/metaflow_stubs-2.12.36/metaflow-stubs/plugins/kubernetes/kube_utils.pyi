######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.12.36                                                                                #
# Generated on 2024-12-07T00:02:15.864200                                                            #
######################################################################################################

from __future__ import annotations


from ...exception import CommandException as CommandException

def parse_cli_options(flow_name, run_id, user, my_runs, echo):
    ...

def qos_requests_and_limits(qos: str, cpu: int, memory: int, storage: int):
    """
    return resource requests and limits for the kubernetes pod based on the given QoS Class
    """
    ...

