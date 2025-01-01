from .BaseController import BaseController 
from fastapi import UploadFile
from models import ResponseSignal
import os

class ProjectController(BaseController):
    
    def __init__(self): # This method is the constructor of the class, it is called when an instance of the class is created
        super().__init__()   # This line is calling the __init__ method of the parent class

    def get_project_path(self, project_id: str):
        
        project_dir = os.path.join(
            self.files_dir, 
            project_id
        )

        if not os.path.exists(project_dir):
            os.makedirs(project_dir)
            
        return project_dir
