from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
import uuid

from app.database.config import get_db
from app.models.user import User as UserModel
from app.schemas.user import User, UserCreate, UserUpdate, UserResponse

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
    summary="Update an existing user",
    responses={
        400: {"description": "Invalid input data"},
        404: {"description": "User not found"}
    }
)
def update_user(
    user_update: UserUpdate,
    user_id: uuid.UUID = Path(..., description="The unique identifier of the user to update."),
    db: Session = Depends(get_db)
):
    """指定されたIDのユーザー情報を更新します。"""
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found."
        )

    # Check if username is being updated and already exists
    if user_update.username and user_update.username != db_user.username:
        existing_username = db.query(UserModel).filter(UserModel.username == user_update.username).first()
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Username '{user_update.username}' already exists."
            )
    
    # Check if email is being updated and already exists
    if user_update.email and user_update.email != db_user.email:
        existing_email = db.query(UserModel).filter(UserModel.email == user_update.email).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Email '{user_update.email}' already exists."
            )

    # Update the fields
    update_data = user_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user


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
