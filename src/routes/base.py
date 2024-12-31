from fastapi import APIRouter
import os  # Import the os module to access environment variables

# Create an instance of the APIRouter class
base_router = APIRouter(
    prefix="/api/v1", # use the /api/v1 prefix for all routes in this file
    tags=["api_v1"],  
    responses={404: {"description": "Not found, check the URL path and try again"}}, # Custom 404 response, if needed
)

# Define a route for the HTTP GET method at the path "/welcome"
@base_router.get("/") # The path is relative to the prefix "/api/v1" defined above
async def welcome(): # the use of async is optional, but recommended for better performance
    app_name = os.getenv("APP_NAME", "") # Get the APP_NAME environment variable or use the default value
    app_version = os.getenv("APP_VERSION", "") # Get the APP_VERSION environment variable or use the default value
    app_description = os.getenv("APP_DESCRIPTION", "") # Get the APP_DESCRIPTION environment variable or use the default value
    app_author = os.getenv("APP_AUTHOR", "") # Get the APP_AUTHOR environment variable or use the default value
    
    # Return a customized JSON response
    return {
        "message": f"Welcome to {app_name}!", # A welcome message
        "details": {
            "name": app_name, # The app name
            "version": app_version, # The app version
            "description": app_description, # The app description
            "author": app_author # The app author
        },
        "note": "Thank you for using our application. If you have any questions, feel free to reach out to our support team."
    }

# --------------------------------------------------------
# ------- Imortant Notes ---------------------------------
# --------------------------------------------------------
# To run the app, use the following command:
# uvicorn main:app --reload --host 0.0.0.0 --port 5000
# use the --reload flag to automatically reload the app when the source code changes
# use the --host flag to specify the host IP address
# use the --port flag to specify the host port number

# The app will be available at http://localhost:5000/api/v1 in your web browser, or you can use curl or Postman to send HTTP requests to the app.
# You can also use the Swagger UI at http://localhost:5000/docs
# Or the ReDoc UI at http://localhost:5000/redoc
# To stop the app, press Ctrl + C in the terminal window where the app is running.
# --------------------------------------------------------
