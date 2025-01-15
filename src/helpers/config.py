from pydantic_settings import BaseSettings, SettingsConfigDict

# Create a Settings class that inherits all the features from BaseSettings.
class Settings(BaseSettings):
    
    # App settings
    APP_NAME: str
    APP_VERSION: str
    APP_DESCRIPTION: str
    APP_AUTHOR: str

    # File settings
    FILE_ALLOWED_TYPES: list
    FILE_MAX_SIZE: int
    FILE_DEFAULT_CHUNK_SIZE: int
    
    # DB Settings
    MONGODB_URI: str
    MONGO_DATABASE: str
    
    # LLM Settings
    GENERATION_BACKEND: str 
    EMBEDDING_BACKEND: str
    
    OPENAI_API_KEY: str = None
    OPENAI_API_URL: str = None
    COHERE_API_KEY: str = None
    
    GENERATION_MODEL_ID: str = None
    EMBEDDING_MODEL_ID: str = None
    EMBEDDING_MODEL_SIZE: str = None
    
    INPUT_DEFAULT_MAX_CHRACTERS: str = None
    GENERATION_DEFAULT_MAX_TOKENS: str = None
    GENERATION_DEFAULT_TEMPERATURE: str = None
    
    class Config(SettingsConfigDict): # Config class inherit from SettingsConfigDict, it's a nested class 
       env_file = ".env" # This tells Pydantic to look for a file named `.env`

def get_settings(): # Function to return object from Settings class
    return Settings()

"""
# ----------------------------------------------------------------------------------------------------------------
What is this code for?
# ----------------------------------------------------------------------------------------------------------------
This code is used to manage application settings like:
- Application name, version, and author information.
- Configuration for files (like maximum size or allowed file types).
- API keys for external services.
- Database connection details.
- ....

# ----------------------------------------------------------------------------------------------------------------
Why Is This Useful?
# ----------------------------------------------------------------------------------------------------------------
Instead of hardcoding settings into the app, which can be messy and insecure, this code:
- Centralizes all settings in one place.
- Validates the settings (ensures they are in the correct format).
- Makes it easy to switch environments (e.g., development, testing, production) by simply changing the .env file.

# ----------------------------------------------------------------------------------------------------------------
What is BaseSettings?
# ----------------------------------------------------------------------------------------------------------------
BaseSettings is a class from the Pydantic library, specifically designed to manage application configurations.
It'sa tool that reads and validates settings for your app.

Usage:
1) Loads settings (or configurations) from multiple sources, such as:
- Environment variables (e.g., os.environ in Python).
- .env files (if specified in the Config class).
- Default values defined in your class (Hardcoded defaults in the class).
2) Validates the settings to ensure they match the expected data types (e.g., str, int, list).
3) Keeps sensitive information safe (like API keys) by not hardcoding them in the code.
 
 
By inheriting BaseSettings, the Settings class automatically:
- Reads settings from environment variables or a .env file.
- Ensures these settings have the correct type and format (If the .env file or environment variables provide incorrect types, BaseSettings will throw an error).
- Example: If APP_NAME is missing or not a string, it will throw an error because APP_NAME is required and must be a string.

# ----------------------------------------------------------------------------------------------------------------
BaseSettings Features:
# ----------------------------------------------------------------------------------------------------------------
1) You can define default values for your settings directly in the Settings class.
Example:
```
class Settings(BaseSettings):
    APP_NAME: str = "DefaultApp"  # Default value (If the .env file doesn’t define APP_NAME, it will use "DefaultApp".)
    APP_VERSION: str = "1.0.0"    # Default value
```

2) Parsing Complex Data Types:
You can also parse more complex data types like lists, dictionaries, or custom objects.
Example:
```
# In .env file =>>> ALLOWED_HOSTS=["localhost", "127.0.0.1", "example.com"]

class Settings(BaseSettings):
    ALLOWED_HOSTS: list = []
```
# ----------------------------------------------------------------------------------------------------------------
The nested Config class
# ----------------------------------------------------------------------------------------------------------------
The nested Config class is a special configuration mechanism in Pydantic. 
It is used to customize the behavior of the parent BaseSettings class.
And it inherits from SettingsConfigDict (a base class provided by Pydantic for defining configuration options).
The Config class is optional, but if present, it modifies how the Settings class works.

Here in the Config class: we tells Pydantic to look for a file named .env in the project's root directory.
Pydantic will then:
1) Parse the .env file.
2) Load its values as environment variables.
3) Use those variables as inputs for the settings in your Settings class.

What Happens Without the Config Class?
If you remove the Config class (or don’t include env_file):
Pydantic will NOT look for a .env file automatically. Instead, it will rely solely on:
- Environment variables already present in the system.
- Default values defined in your Settings class.

Example:
```
class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str = "1.0.0"  # Default value
```
If no environment variables exist:
- APP_NAME will throw an error (because it’s required and has no default value).
- APP_VERSION will use the default value "1.0.0".

# ----------------------------------------------------------------------------------------------------------------
Config class has additional attributes and options you can customize:
# ----------------------------------------------------------------------------------------------------------------

1)  Specify a Custom .env File:
- You can specify a different file name or path for your .env  
```
class Config(SettingsConfigDict):
    env_file = "config.env"  # Use a file named `config.env` instead
```
- Use multiple .env files by providing a list:
```
class Config(SettingsConfigDict):
    env_file = [".env", "production.env"]
```
This allows you to combine environment-specific files.

2)  Allow Environment Variables to Be Prefixed:
- You can use the `env_prefix` option to add a prefix to all environment variables to avoid collisions with other variables.
```
class Config(SettingsConfigDict):
    env_prefix = "MYAPP_"  # All env variables must start with "MYAPP_"

# .env file
MYAPP_APP_NAME=MyApp
MYAPP_APP_VERSION=1.0.0
```

3)  Control Case Sensitivity:
- By default, environment variable names are case-sensitive. You can make them case-insensitive with:
```
class Config(SettingsConfigDict):
    case_sensitive = False  # Environment variables are case-insensitive
```

4)  Ignore Undefined Fields:
- You can configure Pydantic to allow undefined settings (fields not declared in your Settings class) with:
```
class Config(SettingsConfigDict):
    extra = "allow"  # Allow additional fields
```  
"allow": Ignore extra fields.
"forbid": Raise an error if extra fields are found.
"ignore": Silently ignore extra fields.

5) Populate Defaults from a JSON or YAML File:
- Load settings from JSON or YAML files instead of .env.
```
class Config(SettingsConfigDict):
    env_file = "settings.json"
    env_file_encoding = "utf-8"
```
"""






"""
# ----------------------------------------------------------------------------------------------------------------
get_settings() Function:
# ----------------------------------------------------------------------------------------------------------------
The function get_settings() is a helper function that is commonly used to create and return an instance of the Settings class 
(which typically inherits from BaseSettings in Pydantic).

Usage / Importance:
1) Instead of creating a Settings instance manually (Settings()), you call get_settings() wherever you need the settings.
2 Reuse the Same Settings Object: In frameworks like FastAPI, it's common to use this function with a caching mechanism (like @lru_cache) to ensure that the Settings object is created only once and reused for all requests.
Example:
```
from functools import lru_cache
from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "MyApp"
    debug: bool = True

    class Config:
        env_file = ".env"

@lru_cache()  # Ensures the Settings object is cached and reused
def get_settings():
    return Settings()

# Example usage:
settings = get_settings()
print(settings.app_name)  # Outputs the app name loaded from `.env` or default
```



"""


# Note You can manually load .env files using a library like python-dotenv.
# Example:

# from dotenv import load_dotenv
# load_dotenv(".env") # by default it will look for .env file in current directory

# from os import getenv
# APP_NAME = getenv("APP_NAME")
# APP_VERSION = getenv("APP_VERSION")