import os
from faker import Faker
from dotenv import load_dotenv
from pymongo import MongoClient
import random

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "products_db")

fake = Faker()

NUM_PRODUCTS = 150  # cambia el número si quieres más

CATEGORIES = ["botas", "bata", "elemento seguridad", "industrial", "laboratorio"]


def run():
    client = MongoClient(MONGO_URL)
    db = client[MONGO_DB_NAME]
    products_collection = db["products"]

    print(f"Insertando {NUM_PRODUCTS} productos fake...")

    products = []
    for _ in range(NUM_PRODUCTS):
        name = f"Pintura {fake.color_name()}"
        description = fake.sentence(nb_words=8)
        price = round(random.uniform(20000, 120000), 0)
        stock = random.randint(0, 500)
        category = random.choice(CATEGORIES)

        products.append(
            {
                "name": name,
                "description": description,
                "price": price,
                "stock": stock,
                "category": category,
            }
        )

    if products:
        result = products_collection.insert_many(products)
        print(f"Productos insertados: {len(result.inserted_ids)}")
    else:
        print("No se insertó ningún producto.")

    client.close()


if __name__ == "__main__":
    run()
