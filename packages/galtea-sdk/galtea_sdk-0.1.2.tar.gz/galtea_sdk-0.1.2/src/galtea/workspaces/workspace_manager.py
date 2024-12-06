from galtea.datasets.dataset_manager import DatasetManager
from galtea.utils import sanitize_string
import argilla as rg

class WorkspaceManager:
    def __init__(self, client: rg.Argilla):

        self._client = client


    def workspace_exists(self, workspace_name: str) -> bool:

        workspace = self._client.workspaces(workspace_name)

        if workspace:
            return True

        return False

    """
    Given a workspace name, create a new workspace if it doesn't exist
    :param name: name of the workspace
    :return: workspace object
    
    """
    def create_workspace(self, name: str):

        try:
            name = sanitize_string(name)
            workspace = rg.Workspace(
                name=name,
                client=self._client
            )
            workspace = workspace.create()

            print(f"Created workspace {name}")

            return workspace


        except rg._exceptions._api.ConflictError:
            print(f"Workspace {name} already exists")
            return self._client.workspaces(name)
        except Exception as e:
            print(f"Error creating workspace {name}: {e}")
    
    @classmethod
    def get_workspace_manager(cls, client: rg.Argilla, workspace_name: str):
        
        try:
            workspace = client.workspaces(workspace_name)
            return cls(client, workspace)
    
        except Exception as e:
            raise ValueError(f"Workspace {workspace_name} not found") from e

    def get_dataset_manager(self, dataset_name: str):
        return DatasetManager.get_dataset_manager(self._client, dataset_name, self._workspace.name)
    
    def create_dataset(self, dataset_name: str, settings: dict):
        return DatasetManager.create_dataset(self._client, dataset_name, self._workspace.name, settings)