#!/bin/bash
apt update -y
apt install -y docker.io

docker run -d \
  --name orders-postgres \
  -e POSTGRES_DB=ordersdb \
  -e POSTGRES_USER=orders_user \
  -e POSTGRES_PASSWORD=orders_password \
  -p 5432:5432 \
  -v /data/ordersdb:/var/lib/postgresql/data \
  postgres:15
