from pydantic import BaseModel



class Employee(BaseModel):
    employee_id: str
    name: str

class Booking(BaseModel):
    employee_id: str
    car_id: str
    booking_date: str


class UpdateBooking(BaseModel):
    employee_id: str
    previous_booking_date: str
    new_booking_date: str
    car_id: str = None

class Records(BaseModel):
    employee_id: str
    employee_name: str
    car_id: str
    booking_date: str
    last_updated: str
    previous_booking_date: str
    new_booking_date: str


class BookingResponse(BaseModel):
    employee_id: str
    car_id: str
    booking_date: str
    driver_id: str

#needs work also driver needs to be added, see if you can make model for cars and also employee, would be neat if you can create employee through api