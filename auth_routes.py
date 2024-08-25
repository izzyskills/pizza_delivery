from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from werkzeug.security import check_password_hash, generate_password_hash

from database import Session, engine
from models import User
from schemas import LoginModel, SignupModel
from auth import JWTBearer, create_access_token, create_refresh_token, jwt_bearer

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


session = Session(bind=engine)


@auth_router.get("/")
async def hello(token: str = Depends(JWTBearer())):
    return {"message": "Hello World"}


@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user: SignupModel):
    db_email = session.query(User).filter(User.email == user.email).first()
    db_username = session.query(User).filter(User.username == user.username).first()

    if db_email is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with the email already exists",
        )

    if db_username is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usre with the username already exists",
        )

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=generate_password_hash(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff,
    )
    session.add(new_user)
    session.commit()
    return new_user


@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def login(user: LoginModel):
    """
    ## Login a user
    This requires
        ```
            username:str
            password:str
        ```
    and returns a token pair `access` and `refresh`
    """
    db_user = session.query(User).filter(User.username == user.username).first()

    if db_user and check_password_hash(str(db_user.hashed_password), user.password):
        access_token = create_access_token(subject=str(db_user.username))
        refresh_token = create_refresh_token(subject=str(db_user.username))

        response = {"access": access_token, "refresh": refresh_token}

        return jsonable_encoder(response)

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Username Or Password"
    )


@auth_router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh(refresh_token: str):
    """
    ## Refresh a token
    This requires
        ```
            refresh_token:str
        ```
    and returns a new access token
    """
    payload = jwt_bearer.verify_refresh_jwt(jwtoken=refresh_token)
    if payload:
        username = payload.get("sub")
        access_token = create_access_token(subject=username)
        return jsonable_encoder({"access": access_token})
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Token")
