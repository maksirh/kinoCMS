#!/bin/sh

echo "Waiting for postgres..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

python src/manage.py migrate

python src/manage.py collectstatic --noinput

python src/manage.py compilemessages

exec "$@"