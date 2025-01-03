from fastapi import FastAPI       
from routes import base, data    
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings

# Create an instance of the FastAPI class
app = FastAPI() 

@app.on_event("startup")
async def startup_db_client():
    settings = get_settings()
    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URI)
    app.db_client = app.mongo_conn[settings.MONGO_DATABASE]

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongo_conn.close()
    

# to include the base router in the app
app.include_router(base.base_router)  
app.include_router(data.data_router)  
