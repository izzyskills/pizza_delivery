# import os
# from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Optional

# load_dotenv()


class SignupModel(BaseModel):
    id: Optional[int] = Field(default=None)
    username: str
    email: str
    password: str
    is_staff: Optional[bool] = Field(default=False)
    is_active: Optional[bool] = Field(default=True)

    class Config:
        from_attribute = True
        json_schema_extra = {
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

    class Config:
        from_attribute = True
        json_schema_extra = {
            "example": {"username": "john doe", "password": "password"}
        }
