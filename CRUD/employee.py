from databaseConnect import db
import uuid
import random

employee_collection = db["employee_collection"]
employee_names = ["Shahriar", "Ontu", "Anonno", "Robin","Probin," "Kobir"]

#To generate random Employees
for i in range(1,500):
    employee_collection.insert_one({
        "employee_id": str(uuid.uuid4()),  # Generate a unique employee ID
        "name": f"{random.choice(employee_names)}"
    })