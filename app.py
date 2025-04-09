from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.api.user import router as user_router
from app.database.config import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="User Management API",
    version="1.0.0",
    description="A RESTful API for managing users with database integration."
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーターの登録
app.include_router(user_router)

# ルートエンドポイント
@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to the User Management API"}


# Uvicornで実行するためのコード
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
