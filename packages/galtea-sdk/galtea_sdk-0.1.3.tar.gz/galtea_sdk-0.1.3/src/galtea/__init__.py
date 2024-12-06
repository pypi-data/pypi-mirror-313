from typing import Optional
import os
from galtea.connection.sdk_connection import SDKConnection
from galtea.datasets.dataset_manager import DatasetManager
from galtea.models.template_fields import TemplateType
from galtea.templates.concrete import ConcreteTemplateFactory
from galtea.users.user_manager import UserManager
from galtea.workspaces.workspace_manager import WorkspaceManager
from pydantic import BaseModel, Field, ValidationError
from pydantic_core import ErrorDetails 

CUSTOM_MESSAGES = {
    'name': 'Annotation task name must contain only alphanumeric characters, underscores, and hyphens (no spaces allowed)',
    'workspace_name': 'Workspace name must contain only alphanumeric characters, underscores, and hyphens (no spaces allowed)',
}

def convert_errors(
    e: ValidationError, custom_messages: dict[str, str]
) -> list[ErrorDetails]:
    new_errors: list[ErrorDetails] = []
    for error in e.errors():
        custom_message = custom_messages.get(error['loc'][0])
        if custom_message:
            ctx = error.get('ctx')
            error['msg'] = (
                custom_message.format(**ctx) if ctx else custom_message
            )
        new_errors.append(error)
    return new_errors

class AnnotationTaskParams(BaseModel):
    name: str = Field(..., pattern=r'^[a-zA-Z0-9_-]+$')
    workspace_name: str = Field(..., pattern=r'^[a-zA-Z0-9_-]+$')
    template_type: TemplateType = None
    dataset_path: str = "dataset.json"
    min_submitted: Optional[int] = None
    guidelines: Optional[str] = None
    users_path_file: Optional[str] = "users.json"
    show_progress: bool = True
    export_records: bool = True

    
class ArgillaAnnotationTask:

    def __init__(self, argilla_api_url: str = os.getenv("ARGILLA_API_URL"), argilla_api_key: str = os.getenv("ARGILLA_API_KEY")):
        """
        Initialize the ArgillaAnnotationTask class.
        Parameters:
            argilla_api_url (str): The URL of the Argilla API.
            argilla_api_key (str): The API key for the Argilla API.
        """ 

        self._sdk_connection = SDKConnection(argilla_api_url, argilla_api_key)
        self._workspace_manager = WorkspaceManager(self._sdk_connection.client)
        self._user_manager = UserManager(self._sdk_connection.client)
        self._dataset_manager = DatasetManager(self._sdk_connection.client)
        self._template_factory = ConcreteTemplateFactory()


    def create_annotation_task(
        self,
        name: str,
        template_type: TemplateType = None,
        workspace_name: Optional[str] = None,
        dataset_path: str = None,
        min_submitted: Optional[int] = 1,
        guidelines: Optional[str] = "",
        users_path_file: Optional[str] = "users.json",
        show_progress: bool = True,
        export_records: bool = True
    ):
        """
        Create an annotation task with the specified parameters.
        
        Args:
            name (str): Name of the annotation task (alphanumeric, underscores, and hyphens only)
            workspace_name (Optional[str]): Name of the workspace (alphanumeric, underscores, and hyphens only)
            template_type (TemplateType): Type of template to use
            dataset_path (str): Path to the dataset file
            min_submitted (Optional[int]): Minimum number of submissions required
            guidelines (Optional[str]): Guidelines for the annotation task
            users_path_file (Optional[str]): Path to the users JSON file
            show_progress (bool): Whether to show progress after creation
            export_records (bool): Whether to export records when complete
        """

        try:
            workspace_name = name if not workspace_name else workspace_name

            params = AnnotationTaskParams(
                name=name,
                workspace_name=workspace_name,
                template_type=template_type,
                dataset_path=dataset_path,
                min_submitted=min_submitted,
                guidelines=guidelines,
                users_path_file=users_path_file,
                show_progress=show_progress,
                export_records=export_records
            )



            workspace = self._workspace_manager.create_workspace(params.workspace_name)
            
            self._user_manager.create_users(workspace, users_path_file=params.users_path_file)

            template = self._template_factory.get_template(
                params.name,
                params.template_type,
                params.min_submitted,
                params.guidelines
            )
            settings = template.build_settings()
            
            self._dataset_manager.create_dataset(params.name, workspace, settings)
            self._dataset_manager.load_records(template=template, dataset_path=params.dataset_path)

            progress = self._dataset_manager.get_progress()

            if params.show_progress:
                print(f"Dataset progress: {progress}")
        
            if progress['completed'] == progress['total'] and params.export_records:
                from time import strftime
                export_path = f"{self._dataset_manager.dataset.name}_{strftime('%Y-%m-%d_%H-%M-%S')}.json"
                self._dataset_manager.dataset.records.to_json(export_path)
                print(f"Exported dataset to {export_path}")
        except ValidationError as validation_error:
            print(validation_error)
            errors = convert_errors(validation_error, CUSTOM_MESSAGES)
            for error in errors:
                print(f"[ERROR]: {error['msg']}")
        except Exception as e:
            print(f"Error creating annotation task: {e}")
            import traceback
            traceback.print_exc()

    
    def get_progress(self, dataset_name: str, workspace_name: str):
        """
        Given a dataset name and a workspace name, this function returns the progress of annotation of the dataset.
        Parameters:
            dataset_name (str): The name of the dataset.
            workspace_name (str): The name of the workspace.
        Returns:
            dict: The progress of the dataset.
            e.g. returns {'total': 10, 'completed': 0, 'pending': 10}
        """
        return self._dataset_manager.get_progress(dataset_name, workspace_name)
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        pass