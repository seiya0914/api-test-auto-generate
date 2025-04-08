from typing import List, Dict, Optional
from fastapi import FastAPI, HTTPException, status, Path
from pydantic import BaseModel, Field
import uuid

app = FastAPI(
    title="Simple Employee List API",
    version="1.0.0",
    description="An extremely basic API to list, create, and update employees."
)

# --- Pydantic Models ---

class SimpleEmployee(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, description="Unique identifier for the employee.")
    name: str = Field(..., description="Employee's name.")
    department: str = Field(..., description="Employee's department.")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
                "name": "Taro Yamada",
                "department": "Sales"
            }
        }
    }

class SimpleEmployeeUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Employee's updated name.")
    department: Optional[str] = Field(None, description="Employee's updated department.")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Taro Yamada Updated",
                "department": "Sales Updated"
            }
        }
    }


# --- Simple In-Memory "Database" ---
dummy_db: Dict[uuid.UUID, SimpleEmployee] = {}

initial_employees_data = [
    {"name": "Taro Yamada", "department": "Sales"},
    {"name": "Hanako Tanaka", "department": "Engineering"},
    {"name": "Jiro Suzuki", "department": "Marketing"}
]
for emp_data in initial_employees_data:
    employee = SimpleEmployee(**emp_data)
    dummy_db[employee.id] = employee

# --- API Endpoints ---

@app.get(
    "/users",
    response_model=List[SimpleEmployee],
    summary="Get a list of employees",
    tags=["Employees"]
)
def list_employees():
    """従業員のリスト（名前と部署名）を返します。"""
    print("GET /users が呼び出されました")
    return list(dummy_db.values())

@app.post(
    "/users",
    response_model=SimpleEmployee,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new employee",
    tags=["Employees"],
    responses={
        400: {"description": "Invalid input data"}
    }
)
def create_employee(employee_in: SimpleEmployee):
    """新しい従業員を作成し、メモリに追加します。"""
    print(f"POST /users が呼び出されました with data: {employee_in.model_dump()}")

    if employee_in.id in dummy_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Employee with ID {employee_in.id} already exists."
        )

    dummy_db[employee_in.id] = employee_in
    print(f"Employee created with ID: {employee_in.id}")
    return employee_in

@app.put(
    "/users/{user_id}",
    response_model=SimpleEmployee,
    summary="Update an existing employee",
    tags=["Employees"],
    responses={
        400: {"description": "Invalid input data"},
        404: {"description": "Employee not found"}
    }
)
def update_employee(
    employee_update: SimpleEmployeeUpdate,
    user_id: uuid.UUID = Path(..., description="The unique identifier of the employee to update.")
):
    """指定されたIDの従業員の名前と部署名を更新します。"""
    print(f"PUT /users/{user_id} が呼び出されました with data: {employee_update.model_dump()}")

    existing_employee = dummy_db.get(user_id)
    if not existing_employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID {user_id} not found."
        )

    # Update the fields
    update_data = employee_update.model_dump(exclude_unset=True)
    if "name" in update_data:
        existing_employee.name = update_data["name"]
    if "department" in update_data:
        existing_employee.department = update_data["department"]

    print(f"Employee {user_id} updated.")
    return existing_employee


# Uvicornで実行するためのコード (通常はコマンドラインから実行)
# if __name__ == '__main__':
#     import uvicorn
#     uvicorn.run(app, host='0.0.0.0', port=8000)
