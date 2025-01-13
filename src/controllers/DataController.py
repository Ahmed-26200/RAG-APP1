from fastapi import UploadFile
from .BaseController import BaseController
from .ProjectController import ProjectController
from models import ResponseSignal
import os
import re

class DataController(BaseController):
    def __init__(self):
        
        super().__init__() # Call the constructor of the parent class (BaseController)
        
        # Initialize the size_scale attribute
        self.size_scale = 1048576 # = 1024 * 1024 , converting MB to bytes as file.size in UploadFile class (used in validate_uploaded_file) returns the file size in bytes
        r"""
        file.size returns the size of the file in bytes, 
        so we need to convert the FILE_MAX_SIZE from MB to bytes by multiplying it by self.size_scale which is 1024 * 1024 = 1048576 
        """
    def validate_uploaded_file(self, file: UploadFile):
        
        r"""
        This function validates the uploaded file

        Args:
            file: The uploaded file.

        Returns:
            The result of the operation.
        """
        
        # check if the file type is not in the list of allowed file types (existing in the .env file)
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value
        
        # check if the file size is greater than the maximum allowed size
        if file.size > self.app_settings.FILE_MAX_SIZE * self.size_scale:
            return False, ResponseSignal.FILE_SIZE_EXCEEDED.value
        
        r"""
        file.size returns the size of the file in bytes, 
        so we need to convert the FILE_MAX_SIZE from MB to bytes by multiplying it by self.size_scale which is 1024 * 1024 = 1048576 
        """
        
        # if the file is valid, return True
        return True, ResponseSignal.FILE_VALIDATED_SUCCESS.value

    
    def generate_unique_filepath(self, orig_file_name: str, project_id: str):
        
        r"""
        This function generates a unique file name for the uploaded file after removing special characters and replacing spaces with underscores.

        Args:
            orig_file_name: The original file name.
            project_id: The project id.

        Returns:
            A unique file path
        """
        
        # Generate a random string of 12 characters | Output: 12 random characters
        random_key = self.generate_random_string()
        
        # Get the project directory or create it if it does not exist
        # Example output: f:\LLM\LLMProjects\RAG-APP-1\src\assets\files\1
        project_path = ProjectController().get_project_path(project_id=project_id)

        # Remove special characters and replace spaces with underscores
        cleaned_file_name = self.get_clean_file_name(
            orig_file_name=orig_file_name
        )

        # Generate a new file path by joining the project directory with the random string and the cleaned file name
        # Example output: f:\LLM\LLMProjects\RAG-APP-1\src\assets\files\1\mw1178534nx8_Projectname.txt
        new_file_path = os.path.join(
            project_path,
            random_key + "_" + cleaned_file_name
        )

        # Check if the new file path already exists, if it does, generate a new random string and try again.
        while os.path.exists(new_file_path):
            random_key = self.generate_random_string()
            new_file_path = os.path.join(
                project_path,
                random_key + "_" + cleaned_file_name
            )

        return new_file_path, random_key + "_" + cleaned_file_name
    
    
    # Remove special characters and replace spaces with underscores
    def get_clean_file_name(self, orig_file_name: str):
        r"""
        This function cleans the file name by removing special characters and replacing spaces with underscores

        Args:
            orig_file_name: The original file name.
        Returns:
            A cleaned file name
        """
        # remove any special characters, except underscore and .
        cleaned_file_name = re.sub(r'[^\w.]', '', orig_file_name.strip())
        
        r"""
        
        - The regular expression [^\w.] matches any character that is not a word character (letters, digits, or underscore) and not a dot.
        The re.sub function replaces all such characters with an empty string, effectively removing them from the orig_file_name.
        
        - orig_file_name.strip() : Removes any leading and trailing whitespace.
        
        - Example input: " example@file!name.txt "   |   Output: "examplefilename.txt"
        
        """

        # replace spaces with underscore
        # Example input: " example file name.txt "   |   Output: "example_file_name.txt"
        cleaned_file_name = cleaned_file_name.replace(" ", "_")

        return cleaned_file_name