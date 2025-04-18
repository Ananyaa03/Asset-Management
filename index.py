from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
 
# --- 1. MongoDB Connection Details ---
# Replace with your actual MongoDB connection string
MONGODB_URL = "mongodb://localhost:27017"  # Default local connection
DATABASE_NAME = "asset_management_db"  # Choose a name for your database
ASSET_COLLECTION_NAME = "assets"  # Collection to store asset data
 
# --- 2. FastAPI App Initialization ---
app = FastAPI()
 
# --- 3. MongoDB Client Initialization ---
client: AsyncIOMotorClient = None  # Global client instance
 
async def connect_to_mongo():
    global client
    if client is None:  # Check if client is already initialized
        client = AsyncIOMotorClient(MONGODB_URL)
    try:
        await client.admin.command('ping')  # Check connection
        print("Successfully connected to MongoDB")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        # Consider raising an exception here to prevent the app from starting
        # raise  # Uncomment if you want the app to fail on DB connection error
 
async def close_mongo_connection():
    global client
    if client:
        client.close()
        client = None  # Reset to None after closing
        print("Disconnected from MongoDB")
 
# FastAPI startup and shutdown events to handle connection
app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)
 
# --- 4. Helper Function to Get Collection ---
def get_asset_collection():
    """
    Helper function to get the MongoDB collection.  Raises an Exception if the client is not initialized.
    """
    if not client:
        raise Exception("MongoDB client is not initialized.  Ensure the application is running.")
    return client[DATABASE_NAME][ASSET_COLLECTION_NAME]
 
# --- 5. Pydantic Models ---
 
class Asset(BaseModel):
    """
    Pydantic model for representing an asset.  Use Field for more control
    and documentation.
    """
    employee_id: str = Field(..., description="ID of the employee assigned to the asset")
    asset_names: List[str] = Field(..., description="Names of the assets assigned")
    asset_id: List[str] = Field(..., description="Ids of the assets assigned")
    purchase_date: Optional[str] = Field(None, description="Date the asset was purchased (optional)")
    serial_number: Optional[str] = Field(None, description="Serial number of the asset (optional)")
    condition: Optional[str] = Field(None, description="Current condition of the asset (optional)")

 
class AssetInDB(Asset):
    """
    Pydantic model representing an asset as stored in the database.  It includes the `_id`
    field, which is an ObjectId in MongoDB.  We use a string representation in the model.
    """
    id: str = Field(..., description="Unique identifier of the asset in the database")

    @classmethod
    def from_mongo(cls, data):
        """Converts MongoDB document to Pydantic model."""
        if "_id" in data:
            data["id"] = str(data["_id"])
            del data["_id"]
        return cls(**data)

def to_object_id(asset_id: str) -> ObjectId:
    """Converts a string to ObjectId, raises ValueError if invalid."""
    try:
        return ObjectId(asset_id)
    except Exception:
        raise ValueError("Invalid ObjectId format")
 
# --- 6. API Endpoints ---
 
@app.post("/assets/", response_model=AssetInDB, status_code=201)
async def create_asset(asset: Asset):
    """
    Creates a new asset in the database.
    """
    assets_collection = get_asset_collection()
    asset_data = asset.dict()  # Convert Pydantic model to a dictionary
    result = await assets_collection.insert_one(asset_data)
    new_asset = await assets_collection.find_one({"_id": result.inserted_id})
    return AssetInDB.from_mongo(new_asset)  # Use the helper method
 
@app.get("/assets/{asset_id}", response_model=AssetInDB)
async def get_asset(asset_id: str):
    assets_collection = get_asset_collection()
    try:
        object_id = to_object_id(asset_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid asset ID")
    
    asset = await assets_collection.find_one({"_id": object_id})
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    # Convert MongoDB `_id` to string when returning data
    return AssetInDB(id=str(asset["_id"]), **asset)
 
@app.get("/employees/{employee_id}/assets/", response_model=List[AssetInDB])
async def get_employee_assets(employee_id: str):
    """
    Retrieves all assets assigned to a specific employee.
    """
    assets_collection = get_asset_collection()
    assets = await assets_collection.find({"employee_id": employee_id}).to_list(length=None)
    return [AssetInDB.from_mongo(asset) for asset in assets]  # Use the helper
 
@app.put("/assets/{asset_id}", response_model=AssetInDB)
async def update_asset(asset_id: str, asset: Asset):
    """
    Updates an existing asset.
    """
    assets_collection = get_asset_collection()
    try:
        object_id = to_object_id(asset_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid asset ID")
 
    asset_data = {k: v for k, v in asset.dict().items() if v is not None}  # Exclude None values
    if not asset_data:
        raise HTTPException(status_code=400, detail="No fields to update")
 
    result = await assets_collection.update_one({"_id": object_id}, {"$set": asset_data})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Asset not found")
    updated_asset = await assets_collection.find_one({"_id": object_id})
    return AssetInDB.from_mongo(updated_asset)  # Use the helper
 
@app.delete("/assets/{asset_id}", response_model=dict)
async def delete_asset(asset_id: str):
    """
    Deletes an asset.
    """
    assets_collection = get_asset_collection()
    try:
        object_id = to_object_id(asset_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid asset ID")
 
    result = await assets_collection.delete_one({"_id": object_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Asset not found")
    return {"message": "Asset deleted successfully"}
