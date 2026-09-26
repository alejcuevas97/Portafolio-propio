#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

# Crear carpeta de estáticos para Railway
mkdir -p /app/staticfiles

# Ejecutar collectstatic
python manage.py collectstatic --noinput

# Migraciones
python manage.py migrate

# Crear admin si tu comando existe
python manage.py create_admin
