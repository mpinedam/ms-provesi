#!/bin/bash
apt update -y
apt install -y docker.io git
git clone https://github.com/mpinedam/ms-provesi.git /deploy
cd /deploy/ms-orders
docker compose up -d
sleep 10   # espera que la app arranque
docker exec ms-users python seed_orders.py
