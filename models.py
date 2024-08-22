from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    order = relationship("Order", back_populates="user")

    def __str__(self):
        return f"<User> {self.username}"

    def __repr__(self):
        return f"<User> {self.username}"


class Order(Base):
    ORDER_STATUS = (
        ("Pending", "pending"),
        ("Delivered", "delivered"),
        ("IN-TRANSIT", "in-transit"),
    )

    PiZZA_DELIVERY = (
        ("Small", "small"),
        ("Medium", "medium"),
        ("Large", "large"),
        ("Extra Large", "extra-large"),
    )
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer, nullable=False)
    order_status = Column(ChoiceType(choices=ORDER_STATUS), default="Pending")
    pizza_size = Column(ChoiceType(choices=PiZZA_DELIVERY), default="Small")
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="order")

    def __str__(self):
        return f"<Order> {self.id}"

    def __repr__(self):
        return f"<Order> {self.id}"
