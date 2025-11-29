import os
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from pymongo import MongoClient
from bson import ObjectId

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "products_db")

client = MongoClient(MONGO_URL)
db = client[MONGO_DB_NAME]
products_collection = db["products"]

app = FastAPI(title="Products Service", version="0.1.0")


# ====== Helpers ======
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)


# ====== Esquemas Pydantic ======
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = ""
    price: float
    stock: int
    category: str


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: PyObjectId = Field(alias="_id")

    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True


# ====== Endpoints ======

@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok", "service": "products"}


@app.get("/api/products", response_model=List[Product], tags=["products"])
def list_products():
    products = list(products_collection.find())
    return products


@app.post("/api/products", response_model=Product, tags=["products"])
def create_product(product_in: ProductCreate):
    result = products_collection.insert_one(product_in.dict())
    new_product = products_collection.find_one({"_id": result.inserted_id})
    return new_product


@app.get("/api/products/{product_id}", response_model=Product, tags=["products"])
def get_product(product_id: str):
    try:
        oid = ObjectId(product_id)
    except Exception:
        raise HTTPException(status_code=400, detail="product_id inválido")

    product = products_collection.find_one({"_id": oid})
    if not product:
        raise HTTPException(status_code=404, detail=f"Producto con id={product_id} no existe")
    return product
