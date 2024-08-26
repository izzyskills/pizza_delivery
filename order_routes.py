from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi import APIRouter, Depends, status
from models import User, Order
from auth import JWTBearer
from schemas import OrderModel
from database import Session, engine

session = Session(bind=engine)

order_router = APIRouter(
    prefix="/order",
    tags=["order"],
)


@order_router.get("/")
async def hello():
    return {"message": "Hello World"}


@order_router.post("/order")
async def create_order(order: OrderModel, token: str = Depends(JWTBearer())):
    db_user = session.query(User).filter(User.username == token).first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    new_order = Order(
        quantity=order.quantity,
        order_status=order.orderStatus,
        pizza_size=order.pizza_size,
        user_id=db_user.id,
    )
    session.add(new_order)
    session.commit()

    response = {
        "quantity": new_order.quantity,
        "orderStatus": new_order.order_status,
        "pizza_size": new_order.pizza_size,
        "id": new_order.id,
    }
    return jsonable_encoder(response)
