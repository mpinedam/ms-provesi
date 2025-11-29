from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session

from db import Base, engine, SessionLocal, OrderDB

# Crear tablas en la BD (simple por ahora)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Orders Service", version="0.1.0")


# ====== Pydantic schemas ======
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
    new_order = OrderDB(
        user_id=order_in.user_id,
        product_id=order_in.product_id,
        quantity=order_in.quantity,
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order
