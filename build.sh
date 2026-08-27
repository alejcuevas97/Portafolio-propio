#!/usr/bin/env bash
# Render build script.
set -o errexit

pip install -r requirements.txt

npm ci
npm run build:css

python manage.py collectstatic --noinput
python manage.py migrate
python manage.py create_admin
