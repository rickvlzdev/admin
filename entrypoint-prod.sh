#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z admin-db 5432; do
  sleep 0.1
done

echo "PostgreSQL started"

gunicorn -b 0.0.0.0:5002 manage:app