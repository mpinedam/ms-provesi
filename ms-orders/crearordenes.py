import os
import random
import requests
from faker import Faker
from dotenv import load_dotenv

load_dotenv()

ORDERS_SERVICE_URL = os.getenv("ORDERS_SERVICE_URL", "http://3.80.5.29:8080")
USERS_SERVICE_URL = os.getenv("USERS_SERVICE_URL", "http://100.28.123.83:8000/api/users")
PRODUCTS_SERVICE_URL = os.getenv("PRODUCTS_SERVICE_URL", "http://44.200.73.143:8001/api/products")

fake = Faker()

NUM_ORDERS = 10  # ajusta este número según lo que necesites


def get_all_users():
    resp = requests.get(USERS_SERVICE_URL, timeout=5)
    resp.raise_for_status()
    return resp.json()


def get_all_products():
    resp = requests.get(PRODUCTS_SERVICE_URL, timeout=5)
    resp.raise_for_status()
    return resp.json()


def create_order(user_id: int, product_id: str, quantity: int = 1):
    url = f"{ORDERS_SERVICE_URL}/orders"
    payload = {
        "user_id": user_id,
        "product_id": product_id,
        "quantity": quantity,
    }
    resp = requests.post(url, json=payload, timeout=5)
    if resp.status_code not in (200, 201):
        print(f"Error creando orden: status={resp.status_code}, body={resp.text}")
    return resp


def run():
    print("Obteniendo usuarios...")
    users = get_all_users()
    user_ids = [u["id"] for u in users]
    print(f"Usuarios disponibles: {len(user_ids)}")

    print("Obteniendo productos...")
    products = get_all_products()
    product_ids = [p["id"] for p in products]
    print(f"Productos disponibles: {len(product_ids)}")

    if not user_ids or not product_ids:
        print("No hay usuarios o productos suficientes para generar órdenes.")
        return

    print(f"Creando {NUM_ORDERS} órdenes...")
    created = 0

    for _ in range(NUM_ORDERS):
        user_id = random.choice(user_ids)
        product_id = random.choice(product_ids)
        quantity = random.randint(1, 10)

        resp = create_order(user_id, product_id, quantity)
        if resp.status_code in (200, 201):
            created += 1

    print(f"Órdenes creadas correctamente: {created}/{NUM_ORDERS}")


if __name__ == "__main__":
    run()
