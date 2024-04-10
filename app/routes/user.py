from fastapi import APIRouter, Depends, HTTPException
from app.models.user import User
from app.models.login_user import LoginUser
from app.services.user_service import UserService
from app.db import connect_to_pg

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)
user_service = UserService()

@router.post("/register/")
async def register_user(user: User):
    try:
        res_dict =  await user_service.create_user(user)
        print(res_dict["status"])
        if res_dict["status"]:
            return {"message": res_dict["message"]}
        else:
            raise HTTPException(status_code=401, detail=res_dict["message"])
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from fastapi import HTTPException

@router.post("/login/")
async def login_user(login_user: LoginUser):
    try:
        # Check if the email ID is present in the database
        user_data = await user_service.find_user_by_email(login_user.email_id)
        if not user_data:
            # If email ID is not found, raise an HTTPException with status code 404
            raise HTTPException(status_code=404, detail="User not found")

        # Authenticate the user with the provided password
        res_dict = await user_service.authenticate_user(login_user)

        if res_dict["status"]:
            # If authentication is successful, return a success message and token
            return {"message": res_dict["message"], "token": res_dict["token"], "user_id": res_dict["user_id"]}
        else:
            # If authentication fails, raise an HTTPException with status code 401
            raise HTTPException(status_code=401, detail=res_dict["message"])

    except Exception as e:
        # Handle other exceptions (e.g., database errors) and raise an HTTPException with status code 500
        raise HTTPException(status_code=500, detail=str(e))

