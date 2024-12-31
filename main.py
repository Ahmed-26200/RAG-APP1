# Import the FastAPI class from the fastapi module
from fastapi import FastAPI

# Create an instance of the FastAPI class
app = FastAPI()

# Define a route for the HTTP GET method at the path "/welcome"
@app.get("/welcome")
def welcome():
    # Return a JSON response with a welcome message
    return {
        "message": "Welcome to the FastAPI app"
    }

# To run the app, use the following command:
# uvicorn main:app --reload --host 0.0.0.0 --port 5000