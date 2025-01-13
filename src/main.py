"""

For main.py:
- it's preferred to minimize the code in main.py and keep it as simple as possible.
- main.py is the entry point of the application.

"""

from fastapi import FastAPI       

from routes import base_router  
from routes import data_router
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings 

"""
Note:
instead of writing `from routes.base import base_router` we can write `from routes import base_router`
as it's already imported in __init__.py file in routes directory.
"""

# Create an instance(object) of the FastAPI class
app = FastAPI() 

@app.on_event("startup")
async def startup_db_client(): # start database connection
    settings = get_settings()
    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URI) # attach the mongo_conn to the app, so that it can be used in other parts of the app
    app.db_client = app.mongo_conn[settings.MONGO_DATABASE]   # attach the db_client to the app

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongo_conn.close()

app.include_router(base_router)

app.include_router(data_router)

"""
To run the app as a web server, use the following command: uvicorn main:app --reload --host 0.0.0.0 --port 5000
- use the --reload flag to automatically reload the app when the source code changes [Default: False], it's suitable for development purposes and should not be used in production environments as it can cause performance issues and security vulnerabilities.
- use the --host flag to specify the host IP address [Default: 127.0.0.1], The --host 0.0.0.0 flag in the uvicorn command specifies that the server should listen on all available network interfaces. This means that the application will be accessible not only from localhost (127.0.0.1) but also from any external IP address assigned to the machine.
- use the --port flag to specify the host port number [Default: 8000]
- To stop the app, press Ctrl + C in the terminal window where the app is running.
# ----------------------------------------------------------------------------------------------------------------
http://localhost:8000/ or http://127.0.0.1:8000/ is the base URL for the application.
But as we use Port 5000, we have to use http://localhost:5000/ or http://127.0.0.1:5000/
You can use curl or Postman to send HTTP requests to the app.
# ----------------------------------------------------------------------------------------------------------------
You can also use the Swagger UI at http://localhost:5000/docs
Or the ReDoc UI at http://localhost:5000/redoc
Or the OpenAPI JSON at http://localhost:5000/openapi.json
""" 
