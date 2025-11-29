import os
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
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


# ====== Esquemas Pydantic simples (sin tipos raros) ======
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = ""
    price: float
    stock: int
    category: str


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: str   # 👈 devolvemos el _id de Mongo como string


# ====== Helpers para serializar documentos de Mongo ======
def serialize_product(doc) -> dict:
    """
    Convierte un documento de MongoDB a un dict amigable para Product.
    Reemplaza _id (ObjectId) por id (str).
    """
    return {
        "id": str(doc["_id"]),
        "name": doc.get("name", ""),
        "description": doc.get("description", ""),
        "price": doc.get("price", 0),
        "stock": doc.get("stock", 0),
        "category": doc.get("category", ""),
    }


# ====== Endpoints ======

@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok", "service": "products"}


@app.get("/api/products", response_model=List[Product], tags=["products"])
def list_products():
    docs = list(products_collection.find())
    return [serialize_product(d) for d in docs]


@app.post("/api/products", response_model=Product, tags=["products"])
def create_product(product_in: ProductCreate):
    result = products_collection.insert_one(product_in.dict())
    new_doc = products_collection.find_one({"_id": result.inserted_id})
    return serialize_product(new_doc)


@app.get("/api/products/{product_id}", response_model=Product, tags=["products"])
def get_product(product_id: str):
    try:
        oid = ObjectId(product_id)
    except Exception:
        raise HTTPException(status_code=400, detail="product_id inválido")

    doc = products_collection.find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail=f"Producto con id={product_id} no existe")

    return serialize_product(doc)
