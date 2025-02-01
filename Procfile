web: python3 -m gunicorn backend.wsgi
web: gunicorn backend.wsgi --bind 0.0.0.0:8080
gunicorn main:app
release: python manage.py migrate