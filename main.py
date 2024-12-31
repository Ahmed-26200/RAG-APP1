from fastapi import FastAPI

# Load environment variables from the .env file
from dotenv import load_dotenv  
load_dotenv(".env")             

# imort base router from routes folder
from routes import base        

# Create an instance of the FastAPI class
app = FastAPI() 

# to include the base router in the app
app.include_router(base.base_router)  
