from fastapi import APIRouter, HTTPException
from models import DeleteModel
from datetime import datetime
from databaseConnect import bookings


router = APIRouter()

@router.delete("/delete_booking/")
async def delete_booking(delete:DeleteModel):
    booking = await bookings.find_one({
        "employee_id": delete.employee_id, #adsad
        "booking_date": delete.booking_date, #YEAR_MONTH_DATE
    })
    if not booking:
        raise HTTPException(status_code=400, detail="Booking not found")
    if booking is not None:
        if booking["booking_date"] == datetime.today().strftime('%Y-%m-%d'):
            raise HTTPException(status_code=400, detail="Can't change on the booked date")
        else:
            await bookings.delete_one({"_id": booking["_id"]})
            return {"message": "Deleted succesfully"}

