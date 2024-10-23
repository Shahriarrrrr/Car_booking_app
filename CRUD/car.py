from databaseConnect import db
from pymongo import MongoClient
import random
import uuid

# Define the letters list
letters = ["S", "O", "F", "T", "W", "R", "D"]
model= [
    "Ford Mustang",
    "Chevrolet Camaro",
    "Toyota Corolla",
    "Honda Civic",
    "Nissan Altima",
    "BMW 3 Series",
    "Mercedes-Benz C-Class",
    "Audi A4",
    "Volkswagen Jetta",
    "Subaru Impreza",
    "Hyundai Elantra",
    "Kia Forte",
    "Mazda3",
    "Dodge Charger",
    "Tesla Model 3",
    "Porsche 911",
    "Jaguar XE",
    "Lexus IS",
    "Volvo S60",
    "Buick Regal",
    "Chrysler 300",
    "GMC Sierra",
    "Ford F-150",
    "Chevrolet Silverado",
    "Ram 1500",
    "Honda CR-V",
    "Toyota RAV4",
    "Nissan Rogue",
    "Hyundai Tucson",
    "Kia Sportage"
]




car_collection = db['car_collection']

car_collection.insert_one({
    "number_plate": f"{random.randint(0, 100)}{random.choice(letters)}{random.choice(letters)}{random.randint(0, 100)}",
    "model": f"{random.choice(model)}",
    "driver_id": f"{uuid.uuid4()}"
})
for i in range (1,300):
    car_collection.insert_one({
        "number_plate": f"{random.randint(0, 100)}{random.choice(letters)}{random.choice(letters)}{random.randint(0, 100)}",
        "model": f"{random.choice(model)}",
        "driver_id": f"{uuid.uuid4()}"
    })
print("Document inserted.")
