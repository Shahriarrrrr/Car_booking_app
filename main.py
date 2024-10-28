from fastapi import FastAPI
from routes.bookings import router as bookings_router
from routes.employee import router as employee_create_router
from routes.Search_booking_byDate import router as search_history_byDate
from routes.delete_booking import router as delete_booking
from routes.employee_details import router as get_employee
from routes.car_details import router as get_cars



app = FastAPI()

#route
app.include_router(get_employee)
app.include_router(get_cars)
app.include_router(bookings_router)
app.include_router(employee_create_router)
app.include_router(search_history_byDate)
app.include_router(delete_booking)



#H
@app.get("/")
def read_root():
    return {"message": "Welcome to the Booking API!"}
