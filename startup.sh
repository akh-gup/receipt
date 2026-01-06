#!/bin/bash
# wait for Postgres to be ready
echo "Waiting for Postgres..."
until pg_isready -h db -p 5432 -U receipt_user; do
  echo "Waiting for Postgres..."
  sleep 2
done

echo "Postgres is ready. Creating tables..."
python create_tables.py

echo "Inserting initial merchant data..."
python insert_merchants.py

echo "Inserting initial merchant data..."
python insert_merchants_locations.py

echo "Starting FastAPI app..."
uvicorn app.main:app --host 0.0.0.0 --port 8000