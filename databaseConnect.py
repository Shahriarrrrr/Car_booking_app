import asyncio
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
uri = "mongodb+srv://admin:admin@cluster0.evtt2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
my_client = AsyncIOMotorClient(uri)
#my_client = MongoClient("mongodb+srv://admin:admin@cluster0.evtt2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = my_client.company_db
bookings = db["bookings"]
bookings_history = db["booking_history"]
employee_create = db["employee_collection"]
car_collection = db["car_collection"]

#TEST_CHECKS
async def check_collections(db):
    collections = await db.list_collection_names()
    car_info = await bookings_history.find_one({"_id": "6716d0d90e17ddf768bbbab6"})
    booking = await bookings.find_one({
        "employee_id": "0682ed10-7f90-4fd4-bb3d-5a094009c018",
        "booking_date": "6000-12-31",
    })
    records = await bookings.find_one({"booking_date": "9000-12-31"})
    print(booking)
    print(car_info)
    print("Collections in the database:", collections)
    print(records)

async def main():

    await check_collections(db)



# Run the main function
if __name__ == "__main__":
    asyncio.run(main())


