from helpers.config import get_settings, Settings
import os
import random
import string

class BaseController: # This is the parent class for all controllers
    
    def __init__(self): # This method is the constructor of the class, it is called when an instance of the class is created
        
        self.app_settings = get_settings() # Get the app settings from the get_settings function
        
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.files_dir = os.path.join(
            self.base_dir, 
            "assets/files"
            ) # The path to the "files" directory
        
    def generate_random_string(self, length: int=12):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
        
        