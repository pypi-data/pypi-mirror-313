######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.12.35.1+obcheckpoint(0.1.4);ob(v1)                                                   #
# Generated on 2024-12-06T18:19:55.597872                                                            #
######################################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastructures
    import metaflow

from ..datastructures import CheckpointArtifact as CheckpointArtifact
from .constructors import load_checkpoint as load_checkpoint
from .exceptions import CheckpointNotAvailableException as CheckpointNotAvailableException

TYPE_CHECKING: bool

CHECKPOINT_UID_ENV_VAR_NAME: str

DEFAULT_NAME: str

TASK_CHECKPOINTS_ARTIFACT_NAME: str

DEFAULT_STORAGE_FORMAT: str

class Checkpoint(object, metaclass=type):
    def __init__(self, temp_dir_root = None, init_dir = False):
        ...
    @property
    def directory(self):
        ...
    def save(self, path = None, metadata = None, latest = True, name = 'mfchckpt', storage_format = 'files'):
        """
        Saves the checkpoint to the datastore
        
        Parameters
        ----------
        path : Optional[Union[str, os.PathLike]], default: None
            The path to save the checkpoint. Accepts a file path or a directory path.
                - If a directory path is provided, all the contents within that directory will be saved.
                When a checkpoint is reloaded during task retries, `the current.checkpoint.directory` will
                contain the contents of this directory.
                - If a file path is provided, the file will be directly saved to the datastore (with the same filename).
                When the checkpoint is reloaded during task retries, the file with the same name will be available in the
                `current.checkpoint.directory`.
                - If no path is provided then the `Checkpoint.directory` will be saved as the checkpoint.
        
        name : Optional[str], default: "mfchckpt"
            The name of the checkpoint.
        
        metadata : Optional[Dict], default: {}
            Any metadata that needs to be saved with the checkpoint.
        
        latest : bool, default: True
            If True, the checkpoint will be marked as the latest checkpoint.
            This helps determine if the checkpoint gets loaded when the task restarts.
        
        storage_format : str, default: files
            If `tar`, the contents of the directory will be tarred before saving to the datastore.
            If `files`, saves directory directly to the datastore.
        """
        ...
    def __enter__(self):
        ...
    def __exit__(self, exc_type, exc_val, exc_tb):
        ...
    def list(self, name: typing.Optional[str] = None, task: typing.Union["metaflow.Task", str, None] = None, attempt: typing.Union[int, str, None] = None, as_dict: bool = True, within_task: bool = True) -> typing.Iterable[typing.Union[typing.Dict, metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastructures.CheckpointArtifact]]:
        """
        lists the checkpoints in the datastore based on the Task.
        It will always be task scoped.
        
        Usage:
        ------
        
        ```python
        
        Checkpoint().list(name="best") # lists checkpoints in the current task with the name "best"
        Checkpoint().list(task="anotherflow/somerunid/somestep/sometask", name="best") # Identical as the above one but
        Checkpoint().list() # lists all the checkpoints in the current task
        
        ```
        
        Parameters
        ----------
        
        - `name`:
            - name of the checkpoint to filter for
        - `task`:
            - Task object outside the one that is currently set in the `Checkpoint` object; Can be a pathspec string.
        - `attempt`:
            - attempt number of the task (optional filter. If none, then lists all checkpoints from all attempts)
        """
        ...
    def load(self, reference: typing.Union[str, typing.Dict, metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastructures.CheckpointArtifact], path: typing.Optional[str] = None):
        """
        loads a checkpoint reference from the datastore. (resembles a read op)
        
        Parameters
        ----------
        
        `reference` :
            - can be a string, dict or a CheckpointArtifact object:
                - string: a string reference to the checkpoint (checkpoint key)
                - dict: a dictionary reference to the checkpoint
                - CheckpointArtifact: a CheckpointArtifact object reference to the checkpoint
        """
        ...
    ...

