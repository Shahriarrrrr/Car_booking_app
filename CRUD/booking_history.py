from bson.objectid import ObjectId
from datetime import datetime
from databaseConnect import db

bookings = db['booking_collection']
# bookings.insert_one({
#     "employee_id" : "asdada",
#     "car_id" : "adasdasd",
#     "booking_date" : "10-10-2024"
# })

from bson.objectid import ObjectId
from datetime import datetime
from databaseConnect import db

bookings = db['booking_collection']


def create_booking(employee_id, car_id, booking_date):

    # Check employee
    employee = db['employee_collection'].find_one({"employee_id": employee_id})
    if not employee:
        return {"error": "Employee ID does not exist."}

    if datetime.strptime(booking_date, "%Y-%m-%d") <= datetime.now():
        return {"error": "Booking date must be in the future."}

    # Check employee already has a booking
    existing_booking = bookings.find_one({
        "employee_id": employee_id,
        "car_id": car_id,
        "booking_date": booking_date
    })
    if existing_booking:
        return {"error": "Employee already has a booking for this car on this date."}

    # Check if the car is already booked on the specified date
    existing_car_booking = bookings.find_one({"car_id": car_id, "booking_date": booking_date})
    if existing_car_booking:
        return {"error": "Car is already booked on this date."}


    booking = {
        "employee_id": employee_id,
        "car_id": car_id,
        "booking_date": booking_date
    }


    bookings.insert_one(booking)
    return booking


def read_booking(booking_id):

    try:
        booking_object_id = ObjectId(booking_id)
    except Exception:
        return {"error": "Invalid booking ID."}

    booking = bookings.find_one({"_id": booking_object_id})
    if not booking:
        return {"error": "Booking not found."}

    return booking


from datetime import datetime


def update_booking(employee_id, previous_booking_date, new_booking_date, car_id=None):

    booking = bookings.find_one({"employee_id": employee_id, "booking_date": previous_booking_date})
    if not booking:
        return {"error": "Booking not found for the given employee on the specified date."}

    # Check if the previous booking date is today or in the past
    previous_booking_date_dt = datetime.strptime(previous_booking_date, "%Y-%m-%d")
    if previous_booking_date_dt.date() == datetime.now().date():
        return {"error": "Cannot update booking on the booked date."}


    update_fields = {}
    if car_id:
        update_fields["car_id"] = car_id
    if new_booking_date:
        #PAST check
        new_booking_date_dt = datetime.strptime(new_booking_date, "%Y-%m-%d")
        if new_booking_date_dt < datetime.now():
            return {"error": "Cannot set booking date in the past."}
        update_fields["booking_date"] = new_booking_date

    # Update
    if update_fields:
        bookings.update_one({"employee_id": employee_id, "booking_date": previous_booking_date},
                            {"$set": update_fields})
        return {"message": "Booking updated successfully."}
    else:
        return {"message": "No fields to update."}


def delete_booking(booking_id):

    try:
        booking_object_id = ObjectId(booking_id)
    except Exception:
        return {"error": "Invalid booking ID."}

    result = bookings.delete_one({"_id": booking_object_id})
    if result.deleted_count == 0:
        return {"error": "Booking not found."}

    return {"message": "Booking deleted successfully."}
