from typing import List
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Simple Employee List API",
    version="1.0.0",
    description="An extremely basic API to list employees."
)

# --- Pydantic Model ---

class SimpleEmployee(BaseModel):
    name: str
    department: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Taro Yamada",
                "department": "Sales"
            }
        }
    }

# --- Dummy Data ---

dummy_employees: List[SimpleEmployee] = [
    SimpleEmployee(name="Taro Yamada", department="Sales"),
    SimpleEmployee(name="Hanako Tanaka", department="Engineering"),
    SimpleEmployee(name="Jiro Suzuki", department="Marketing")
]

# --- API Endpoint ---

@app.get(
    "/users",
    response_model=List[SimpleEmployee],
    summary="Get a list of employees",
    tags=["Employees"]
)
def list_employees():
    """従業員のリスト（名前と部署名）を返します。"""
    print("GET /users が呼び出されました")
    return dummy_employees

# Uvicornで実行するためのコード (通常はコマンドラインから実行)
# if __name__ == '__main__':
#     import uvicorn
#     uvicorn.run(app, host='0.0.0.0', port=8000)
