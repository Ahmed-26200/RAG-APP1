from fastapi import FastAPI       
from routes import base, data    

# Create an instance of the FastAPI class
app = FastAPI() 

# to include the base router in the app
app.include_router(base.base_router)  
app.include_router(data.data_router)  
