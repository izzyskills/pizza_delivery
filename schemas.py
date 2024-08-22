# import os
# from dotenv import load_dotenv
from pydantic import BaseModel, StrictStr
from typing import Optional

# load_dotenv()


class Settings(BaseModel):
    authjwt_secret_key: StrictStr = (
        "111b19c1e7f168a2ba0216cab4f708262a325f8ff23f34fff209332f432e6113"
    )


class SignupModel(BaseModel):
    id: Optional[int]
    username: str
    email: str
    password: str
    is_staff: Optional[bool]
    is_active: Optional[bool]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "john doe",
                "email": "johndoe@gmail.om",
                "password": "password",
                "is_staff": False,
                "is_active": True,
            }
        }


class LoginModel(BaseModel):
    username: str
    password: str
