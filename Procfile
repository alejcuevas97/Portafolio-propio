web: mkdir -p staticfiles && python manage.py collectstatic --noinput && python manage.py migrate && gunicorn Portafolio.wsgi:application --bind 0.0.0.0:$PORT
