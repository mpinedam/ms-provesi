#!/bin/bash
apt update -y
apt install -y docker.io git
git clone https://github.com/mpinedam/ms-provesi.git /deploy
cd /deploy/api-gateway
docker compose up -d
