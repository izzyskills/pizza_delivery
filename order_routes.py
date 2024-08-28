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


@order_router.get("/orders")
async def list_all_orders(token: str = Depends(JWTBearer())):
    db_user = session.query(User).filter(User.username == token).first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    if bool(db_user.is_staff):
        orders = session.query(Order).all()
        return jsonable_encoder(orders)
    orders = session.query(Order).filter(Order.user_id == db_user.id).all()
    return jsonable_encoder(orders)


@order_router.get("/order/{order_id}")
async def get_order(order_id: int, token: str = Depends(JWTBearer())):
    db_user = session.query(User).filter(User.username == token).first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    order = session.query(Order).filter(Order.id == order_id).first()
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    if order.user_id != db_user.id and not bool(db_user.is_staff):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to view this order",
        )
    return jsonable_encoder(order)


@order_router.put("/order/{order_id}")
async def update_order(
    order_id: int, order: OrderModel, token: str = Depends(JWTBearer())
):
    db_user = session.query(User).filter(User.username == token).first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    db_order = session.query(Order).filter(Order.id == order_id).first()
    if db_order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    if db_order.user_id != db_user.id and not bool(db_user.is_staff):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to update this order",
        )
    db_order.quantity = order.quantity
    db_order.order_status = order.orderStatus
    db_order.pizza_size = order.pizza_size
    session.commit()
    return jsonable_encoder(db_order)


@order_router.delete("/order/{order_id}")
async def delete_order(order_id: int, token: str = Depends(JWTBearer())):
    db_user = session.query(User).filter(User.username == token).first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    db_order = session.query(Order).filter(Order.id == order_id).first()
    if db_order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    if db_order.user_id != db_user.id and not bool(db_user.is_staff):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to delete this order",
        )
    session.delete(db_order)
    session.commit()
    return {"message": "Order deleted successfully"}


@order_router.put("/order/status/{order_status}")
async def update_order_status(
    order_status: str, order_id: int, token: str = Depends(JWTBearer())
):
    db_user = session.query(User).filter(User.username == token).first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    db_order = session.query(Order).filter(Order.id == order_id).first()
    if db_order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    if not bool(db_user.is_staff):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to update this order",
        )
    db_order.order_status = order_status
    session.commit()
    return jsonable_encoder(db_order)
