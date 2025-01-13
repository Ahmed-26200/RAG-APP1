from .BaseController import BaseController 
from fastapi import UploadFile
from models import ResponseSignal
import os

class ProjectController(BaseController):
    
    def __init__(self): # This method is the constructor of the class, it is called when an instance of the class is created
        super().__init__()   # This line is calling the __init__ method of the parent class

    def get_project_path(self, project_id: str):
        
        """
        This function check if the file (project_id) directory exists, if not we need to create the directory

        Args:
            project_id: The uploaded file id.

        Returns:
            The result of the operation.
        """
        
        # Get the assets/files directory and join it with the project_id. 
        # Ex: f:\LLM\LLMProjects\RAG-APP-1\src\assets\files\{1}
        project_dir = os.path.join(
            self.files_dir, 
            project_id
        )

        # If the directory does not exist, we need to create it
        # Ex: if directory 1 does not exist, we need to create it
        if not os.path.exists(project_dir):
            os.makedirs(project_dir)
            
        return project_dir
