import os
import django
from faker import Faker
import random

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "users_service.settings")
django.setup()

from users.models import User  # noqa: E402

fake = Faker()

NUM_USERS = 200  # cambia este número si quieres más o menos


def run():
    print(f"Creando {NUM_USERS} usuarios fake...")
    created = 0

    for _ in range(NUM_USERS):
        name = fake.name()
        email = fake.unique.email()

        # Evitar duplicados raros si ya habías corrido el script
        if User.objects.filter(email=email).exists():
            continue

        User.objects.create(
            name=name,
            email=email,
        )
        created += 1

    print(f"Usuarios creados: {created}")


if __name__ == "__main__":
    run()
