#!/bin/bash
apt update -y
apt install -y docker.io
docker run -d -p 27017:27017 mongo:6