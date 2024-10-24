from databaseConnect import db,bookings
from pymongo.errors import PyMongoError
from fastapi import APIRouter, HTTPException
from models import BookingResponse
from typing import List
from datetime import datetime

router = APIRouter()

@router.get("/search_history/", response_model=List[BookingResponse])
async def search(date: str):
    # Validate the date format
    try:
        search_date = datetime.strptime(date, "%Y-%m-%d").date() # date object
        search_date_str = search_date.strftime("%Y-%m-%d")  # to string
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    try:

        records = await bookings.find({"booking_date": search_date_str}).to_list(None)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query error: {str(e)}")

    if not records:
        raise HTTPException(status_code=404, detail="No bookings found for the specified date.")


    for record in records:
        record["_id"] = str(record["_id"])
        record["car_id"] = str(record["car_id"])
        # Ensure driver_id is included in the response
        if "driver_id" not in record:
            record["driver_id"] = None

    return records


