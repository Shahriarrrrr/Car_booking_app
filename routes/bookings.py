from fastapi import APIRouter, HTTPException
from datetime import datetime,date
from models import Booking, UpdateBooking, Records, Employee
from databaseConnect import db, bookings, bookings_history, car_collection,employee_create
from bson import ObjectId

router = APIRouter()


@router.post("/bookings/history")
async def record_create(booking_doc, is_update=False, previous_booking_date=None, last_updated = f"{datetime.now()}"):
    today_date_iso = datetime.now().isoformat()
    record = {
        "employee_id": booking_doc["employee_id"],
        "car_id": booking_doc["car_id"],
        "booking_date": booking_doc["booking_date"],
        "last_updated": today_date_iso,
        "previous_booking_date": previous_booking_date,
        "new_booking_date": booking_doc["booking_date"] if is_update else None
    }
    await bookings_history.insert_one(record)

@router.post("/bookings/")
async def create_booking(booking: Booking):
    # Check if the employee exists
    employee = await employee_create.find_one({"employee_id": booking.employee_id})
    if not employee:
        raise HTTPException(status_code=404, detail="Employee ID does not exist.")
    booking_datetime_obj = datetime.strptime(booking.booking_date, "%Y-%m-%d")
    #booking_date_obj = booking_datetime_obj.date()
    # Check if the booking date is in the future
    if booking_datetime_obj.date() <= date.today():
        raise HTTPException(status_code=400, detail="Booking date must be in the future.")

    # Check for employee on same date booking
    existing_booking = await bookings.find_one({
        "employee_id": booking.employee_id,
        "car_id": booking.car_id,
        "booking_date": booking_datetime_obj,  #ch
    })

    print(f"Checking for existing booking: Employee ID: {booking.employee_id}, Car ID: {booking.car_id}, Date: {booking.booking_date}")

    if existing_booking:
        raise HTTPException(status_code=400, detail="Employee already has a booking for this car on this date.")

    # Check if the car is already booked on the specified date
    existing_car_booking = await bookings.find_one({"car_id": booking.car_id, "booking_date": booking_datetime_obj})
    if existing_car_booking:
        raise HTTPException(status_code=400, detail="Car is already booked on this date.")

    # Convert car_id to ObjectId
    try:
        car_id_object = ObjectId(booking.car_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid car ID format.")

    # Get car info to fetch the driver ID
    car_info = await car_collection.find_one({"_id": car_id_object})
    if not car_info:
        raise HTTPException(status_code=404, detail="Car not found.")

    # Fetch driver ID from car_info
    driver_id = car_info.get("driver_id")
    if not driver_id:
        raise HTTPException(status_code=400, detail="Driver missing for the selected car.")

    # Create the booking document with driver ID
    booking_doc = {
        "employee_id": booking.employee_id,
        "car_id": booking.car_id,
        "booking_date": booking_datetime_obj,  #STRING hisebe #ch
        "driver_id": driver_id  # Automatically include driver_id from car_info
    }

    # Inserting in the Database
    result = await bookings.insert_one(booking_doc)
    booking_doc["_id"] = str(result.inserted_id)

    await record_create(booking_doc)
    return {"message": "Booking created successfully.", "booking": booking_doc}


@router.put("/bookings/update/")
async def update_booking(update_booking: UpdateBooking):
    prev_datetime_obj = datetime.strptime(update_booking.previous_booking_date, "%Y-%m-%d")
    new_datetime_obj = datetime.strptime(update_booking.new_booking_date, "%Y-%m-%d")

    # Fetch the booking for the employee based on the previous booking date
    booking = await bookings.find_one({
        "employee_id": update_booking.employee_id,
        "booking_date": prev_datetime_obj
    })

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found for the given employee on the specified date.")


    #previous_booking_date_dt = datetime.strptime(update_booking.previous_booking_date, "%Y-%m-%d")
    today = date.today()
    today_dateandtime = datetime.combine(today,datetime.min.time())
    if prev_datetime_obj <= today_dateandtime:
        raise HTTPException(status_code=400, detail="Cannot update booking on the booked date or in the past.")


    update_fields = {}


    if update_booking.car_id is not None:
        # Convert car_id to ObjectId
        try:
            #car_id_object = ObjectId(update_booking.car_id)
            update_fields["car_id"] = update_booking.car_id
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid car ID format.")


    if update_booking.new_booking_date:

        # new_booking_date_dt = datetime.strptime(update_booking.new_booking_date, "%Y-%m-%d")
        if new_datetime_obj < today_dateandtime:
            raise HTTPException(status_code=400, detail="Cannot set booking date in the past.")


        existing_car_booking = await bookings.find_one({
            "car_id": update_fields.get("car_id", str(booking["car_id"])),
            "booking_date": new_datetime_obj
        })
        if existing_car_booking:
            raise HTTPException(status_code=400, detail="The car is already booked on the new date.")

        update_fields["booking_date"] = new_datetime_obj


    if update_fields:
        await bookings.update_one(
            {"employee_id": update_booking.employee_id, "booking_date": prev_datetime_obj},
            {"$set": update_fields}
        )


        await record_create({
            "employee_id": update_booking.employee_id,
            "car_id": update_fields.get("car_id", str(booking["car_id"])),
            "booking_date": update_fields.get("booking_date", new_datetime_obj)
        }, is_update=True, previous_booking_date=prev_datetime_obj)

        return {"message": "Booking updated successfully."}
    else:
        return {"message": "No fields to update."}