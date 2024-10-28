from fastapi import APIRouter, HTTPException
from models import DeleteModel
from datetime import datetime,date
from databaseConnect import bookings


router = APIRouter()

@router.delete("/delete_booking/")
async def delete_booking(delete:DeleteModel):
    booking = await bookings.find_one({
        "employee_id": delete.employee_id, #adsad
        "booking_date": datetime.strptime(delete.booking_date, "%Y-%m-%d").replace(hour = 0,minute = 0, second=0), #YEAR_MONTH_DATE
    })
    if not booking:
        raise HTTPException(status_code=400, detail="Booking not found")
    if booking is not None:
        today = date.today()
        today_dateandtime = datetime.combine(today,datetime.min.time())
        if booking["booking_date"] == today_dateandtime:
            raise HTTPException(status_code=400, detail="Can't change on the booked date")
        else:
            await bookings.delete_one({"_id": booking["_id"]})
            return {"message": "Deleted succesfully"}

