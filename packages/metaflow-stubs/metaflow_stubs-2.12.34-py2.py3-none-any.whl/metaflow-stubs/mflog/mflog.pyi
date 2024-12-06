######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.12.34                                                                                #
# Generated on 2024-12-04T14:12:34.666774                                                            #
######################################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import datetime


VERSION: bytes

RE: bytes

class MFLogline(tuple, metaclass=type):
    """
    MFLogline(should_persist, version, utc_tstamp_str, logsource, id, msg, utc_tstamp)
    """
    @staticmethod
    def __new__(_cls, should_persist, version, utc_tstamp_str, logsource, id, msg, utc_tstamp):
        """
        Create new instance of MFLogline(should_persist, version, utc_tstamp_str, logsource, id, msg, utc_tstamp)
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

ISOFORMAT: str

MISSING_TIMESTAMP: datetime.datetime

MISSING_TIMESTAMP_STR: str

def utc_to_local(x):
    ...

def decorate(source, line, version = b'0', now = None, lineid = None):
    ...

def is_structured(line):
    ...

def parse(line):
    ...

def set_should_persist(line):
    ...

def unset_should_persist(line):
    ...

def refine(line, prefix = None, suffix = None):
    ...

def merge_logs(logs):
    ...

