from fastapi import APIRouter
from databaseConnect import car_collection
from bson import ObjectId


router = APIRouter()

@router.get("/getCar/{id}/")
async def get_car_details(id: str):
    data = await car_collection.find_one({"_id": ObjectId(id)})
    return {
        "car_id": str(data["_id"]),
        "model": data["model"],
        "number_plate": data["number_plate"],
        "driver_id": data["driver_id"],
        #"booked_details":
    }
