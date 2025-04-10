from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
import uuid
from datetime import datetime
import logging

from app.database.config import get_db
from app.models.user import User as UserModel
from app.schemas.user import User, UserCreate, UserUpdate, UserResponse, ErrorResponse

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/",
    response_model=List[UserResponse],
    summary="Get a list of users",
)
def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """ユーザーのリストを返します。"""
    users = db.query(UserModel).offset(skip).limit(limit).all()
    return users


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    responses={
        400: {"description": "Invalid input data"}
    }
)
def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db)
):
    """新しいユーザーを作成し、データベースに追加します。"""
    # Check if username or email already exists
    existing_username = db.query(UserModel).filter(UserModel.username == user_in.username).first()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Username '{user_in.username}' already exists."
        )
    
    existing_email = db.query(UserModel).filter(UserModel.email == user_in.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email '{user_in.email}' already exists."
        )

    # Create new user
    db_user = UserModel(
        username=user_in.username,
        email=user_in.email,
        full_name=user_in.full_name,
        department=user_in.department
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get a specific user by ID",
    responses={
        404: {"description": "User not found"}
    }
)
def get_user(
    user_id: uuid.UUID = Path(..., description="The unique identifier of the user to retrieve."),
    db: Session = Depends(get_db)
):
    """指定されたIDのユーザー情報を返します。"""
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found."
        )
    return db_user


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    responses={
        404: {"description": "User not found", "model": ErrorResponse},
        400: {"description": "Invalid input data", "model": ErrorResponse},
    },
    summary="Update an existing user",
)
def update_user(
    user_id: uuid.UUID,
    user_update: UserUpdate,
    db: Session = Depends(get_db)
):
    """指定されたIDのユーザー情報を更新します。"""
    try:
        # 無効な入力値のチェック
        if user_update.username is not None and len(user_update.username) > 100:
            raise HTTPException(status_code=400, detail="Username is too long")
        if user_update.email is not None and len(user_update.email) > 255:
            raise HTTPException(status_code=400, detail="Email is too long")
        if user_update.full_name is not None and len(str(user_update.full_name)) > 255:
            raise HTTPException(status_code=400, detail="Full name is too long")
        if user_update.department is not None and len(str(user_update.department)) > 255:
            raise HTTPException(status_code=400, detail="Department is too long")
            
        # ユーザーの存在確認
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # 更新するフィールドを設定
        update_data = user_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, value)
        
        user.updated_at = datetime.now()
        db.commit()
        db.refresh(user)
        return user
    except ValueError as e:
        # UUIDの形式エラーなど
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # その他の予期しないエラー
        logger.error(f"Error updating user: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid input data")


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a user",
    responses={
        404: {"description": "User not found"}
    }
)
def delete_user(
    user_id: uuid.UUID = Path(..., description="The unique identifier of the user to delete."),
    db: Session = Depends(get_db)
):
    """指定されたIDのユーザーを削除します。"""
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found."
        )
    
    db.delete(db_user)
    db.commit()
    return None
