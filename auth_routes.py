from fastapi import APIRouter, status
from database import Session,engine
from schemas import SignupModel,LoginModel
from fastapi.exceptions import HTTPException

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


session = Session(bind=engine)

@auth_router.get("/")
async def hello():
    return {"message": "Hello World"}


@auth_router.post("/signup")
async def signup(user: SignupModel):
    db_email = session.query(User).filter(User.email == user.email).first()
    db_username = session.query(User).filter(User.username == user.username).first()

    if db_email is not None:
        return HttpResponse(status_code=status.HTTP_400_BAD_REQUEST, detail="Usre with the Email already exists")
    
    if db_username is not None:
        return HttpResponse(status_code=status.HTTP_400_BAD_REQUEST, detail="Usre with the username already exists")

    new_user = User(username=user.username,email=user.email,password=user.password)
    session.add(user)
    session.commit()
    return user
    
