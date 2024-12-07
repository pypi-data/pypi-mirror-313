######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.12.35.1+obcheckpoint(0.1.4);ob(v1)                                                   #
# Generated on 2024-12-06T18:19:55.621121                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.exception

from ......exception import MetaflowException as MetaflowException

class CheckpointNotAvailableException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, message):
        ...
    ...

class CheckpointException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, message):
        ...
    ...

