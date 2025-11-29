import os
import requests
from typing import List

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db import Base, engine, SessionLocal, OrderDB

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Orders Service", version="0.1.0")

USERS_SERVICE_URL = os.getenv("USERS_SERVICE_URL", "http://localhost:8000/api/users")
PRODUCTS_SERVICE_URL = os.getenv("PRODUCTS_SERVICE_URL", "http://localhost:8001/api/products")


class Order(BaseModel):
    id: int
    user_id: int
    product_id: str   # 👈 string
    quantity: int

    class Config:
        orm_mode = True


class OrderCreate(BaseModel):
    user_id: int
    product_id: str   # 👈 string (id de Mongo)
    quantity: int


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_user_exists(user_id: int) -> None:
    url = f"{USERS_SERVICE_URL}/{user_id}/"  # 👈 Django usa slash final
    try:
        resp = requests.get(url, timeout=3)
    except requests.exceptions.RequestException:
        raise HTTPException(
            status_code=502,
            detail="No se pudo contactar al servicio de usuarios (ms-users)",
        )

    if resp.status_code == 404:
        raise HTTPException(
            status_code=400,
            detail=f"El usuario con id={user_id} no existe",
        )
    elif resp.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail="Error al consultar el servicio de usuarios",
        )


def check_product_exists(product_id: str) -> None:
    url = f"{PRODUCTS_SERVICE_URL}/{product_id}"  # 👈 FastAPI sin slash al final
    try:
        resp = requests.get(url, timeout=3)
    except requests.exceptions.RequestException:
        raise HTTPException(
            status_code=502,
            detail="No se pudo contactar al servicio de productos (ms-product)",
        )

    if resp.status_code == 404:
        raise HTTPException(
            status_code=400,
            detail=f"El producto con id={product_id} no existe",
        )
    elif resp.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail="Error al consultar el servicio de productos",
        )


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok", "service": "orders"}


@app.get("/orders", response_model=List[Order], tags=["orders"])
def list_orders(db: Session = Depends(get_db)):
    orders = db.query(OrderDB).all()
    return orders


@app.post("/orders", response_model=Order, tags=["orders"])
def create_order(order_in: OrderCreate, db: Session = Depends(get_db)):
    check_user_exists(order_in.user_id)
    check_product_exists(order_in.product_id)

    new_order = OrderDB(
        user_id=order_in.user_id,
        product_id=order_in.product_id,
        quantity=order_in.quantity,
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order
