from models import Employee
from databaseConnect import db,employee_create
from pymongo.errors import PyMongoError
from fastapi import APIRouter, HTTPException


router = APIRouter()

@router.post("/creates/create_employee")
async def create_employee(employee: Employee):
    try:
        data = {
            "employee_id": employee.employee_id,
            "name": employee.name
        }
        result = await employee_create.insert_one(data)
        if result.acknowledged:
            return {"Message": "success"}
        else:
            return {"Invalid data , Try again"}

    except PyMongoError as e:
        return {"Message:" f"{e}"}
