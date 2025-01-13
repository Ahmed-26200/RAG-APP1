from helpers.config import Settings, get_settings
import os, random, string

class BaseController:
    def __init__(self):

        self.app_settings = get_settings()

        # navigates up to the "/src" directory  |  Output: f:\LLM\LLMProjects\RAG-APP-1\src
        self.base_dir = os.path.dirname(os.path.dirname(__file__))

        # Then navigates down to the "/src/assets/files" directory  |  Output: f:\LLM\LLMProjects\RAG-APP-1\src\assets\files
        self.files_dir = os.path.join(
            self.base_dir, 
            "assets/files"
            )
        
    def generate_random_string(self, length: int=12):
        """
        This function Generate a random string of the specified length

        Args:
            length (int, optional): The length of the random string to be generated. Defaults to 12.

        Returns:
            str: The generated random string.
        """
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))










r"""
To navigates up the directory tree by using os.path.dirname repeatedly:

`os.path.dirname(__file__)`
This returns the directory containing the current file (parent directory of the file).
# Output: f:\LLM\LLMProjects\RAG-APP-1\src\controllers

`os.path.dirname(os.path.dirname(__file__))`
This returns the directory containing the parent directory (grandparent directory).
# Output: f:\LLM\LLMProjects\RAG-APP-1\src

`os.path.dirname(os.path.dirname(os.path.dirname(__file__)))`
This returns the directory containing the grandparent directory (great-grandparent directory).
# Output: f:\LLM\LLMProjects\RAG-APP-1

`os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))`
This returns the directory containing the great-grandparent directory.
# Output: f:\LLM\LLMProjects

--------------------------------------------------------------------------------
Suggestion for Readability:
--------------------------------------------------------------------------------
If the code is used frequently or for many levels, consider using a helper function to make it cleaner and more dynamic:
```
import os

def get_ancestor_directory(file, levels=1):
    directory = file
    for _ in range(levels):
        directory = os.path.dirname(directory)
    return directory

# Example usage
print(get_ancestor_directory(__file__, 1))  # Parent directory
print(get_ancestor_directory(__file__, 2))  # Grandparent directory
print(get_ancestor_directory(__file__, 3))  # Great-grandparent directory
print(get_ancestor_directory(__file__, 4))  # Great-great-grandparent directory
```
This approach avoids deeply nested calls and makes it easy to adjust the number of levels dynamically.

--------------------------------------------------------------------------------
To navigate down the directory tree (move into child directories)
--------------------------------------------------------------------------------
you can use `os.path.join` to append directory names to the current path.

Example Code for Navigating to Child Directories:
```
import os

def get_descendant_directory(base_dir, *subdirs):

    return os.path.join(base_dir, *subdirs)

# Example usage
current_directory = os.path.dirname(__file__)

# Navigate to a specific child directory
child_directory = get_descendant_directory(current_directory, "child")
grandchild_directory = get_descendant_directory(current_directory, "child", "grandchild")
great_grandchild_directory = get_descendant_directory(current_directory, "child", "grandchild", "great_grandchild")

print("Child Directory:", child_directory)
print("Grandchild Directory:", grandchild_directory)
print("Great-Grandchild Directory:", great_grandchild_directory)
```
os.path.join(base_dir, *subdirs): Combines the base_dir with the provided subdirectories (*subdirs). 
The * syntax allows you to pass multiple subdirectory names dynamically.
 
"""
