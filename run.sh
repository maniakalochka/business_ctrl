#!/bin/bash

cd services/auth && docker compose up --build &
cd ..
cd teams_org && docker compose up --build &

echo "All services are starting..."