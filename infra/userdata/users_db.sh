#!/bin/bash
apt update -y
apt install -y docker.io

docker run -d \
  --name users-postgres \
  -e POSTGRES_DB=usersdb \
  -e POSTGRES_USER=users_user \
  -e POSTGRES_PASSWORD=users_password \
  -p 5432:5432 \
  -v /data/usersdb:/var/lib/postgresql/data \
  postgres:15
