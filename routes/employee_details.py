from fastapi import APIRouter
from databaseConnect import employee_create


router = APIRouter()

@router.get("/getEmployee/{id}/")
async def Get_employee_details(id : str):
    data = await employee_create.find_one({"employee_id" : id})
    return {
        "employee_id": data["employee_id"],
        "employee_name": data["name"]
    }
