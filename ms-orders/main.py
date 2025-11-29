import os
import requests
from typing import List

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db import Base, engine, SessionLocal, OrderDB

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Orders Service", version="0.1.0")

# ====== Config de otros microservicios ======
USERS_SERVICE_URL = os.getenv("USERS_SERVICE_URL", "http://localhost:8000/api/users")
PRODUCTS_SERVICE_URL = os.getenv("PRODUCTS_SERVICE_URL", "http://localhost:8001/api/products")


# ====== Esquemas Pydantic ======
class Order(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int

    class Config:
        orm_mode = True


class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int


# ====== Dependencia de DB ======
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ====== Funciones para validar con otros microservicios ======
def check_user_exists(user_id: int) -> None:
    """
    Llama al microservicio ms-users para verificar si el usuario existe.
    Espera que ms-users exponga /api/users/<id>/
    """
    url = f"{USERS_SERVICE_URL}/{user_id}/"  # ejemplo: http://localhost:8000/api/users/1/
    try:
        resp = requests.get(url, timeout=3)
    except requests.exceptions.RequestException:
        # No se pudo conectar al microservicio
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


def check_product_exists(product_id: int) -> None:
    """
    Llama al microservicio ms-product para verificar si el producto existe.
    Espera que ms-product exponga /api/products/<id>/
    """
    url = f"{PRODUCTS_SERVICE_URL}/{product_id}"  # ejemplo: http://localhost:8001/api/products/10/
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


# ====== Endpoints ======
@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok", "service": "orders"}


@app.get("/orders", response_model=List[Order], tags=["orders"])
def list_orders(db: Session = Depends(get_db)):
    orders = db.query(OrderDB).all()
    return orders


@app.post("/orders", response_model=Order, tags=["orders"])
def create_order(order_in: OrderCreate, db: Session = Depends(get_db)):
    # 1️⃣ Validar que el usuario exista en ms-users
    check_user_exists(order_in.user_id)

    # 2️⃣ Validar que el producto exista en ms-product
    check_product_exists(order_in.product_id)

    # 3️⃣ Si todo bien, crear la orden en nuestra BD local
    new_order = OrderDB(
        user_id=order_in.user_id,
        product_id=order_in.product_id,
        quantity=order_in.quantity,
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order
