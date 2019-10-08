release: python manage.py migrate --fake
release: python manage.py makemigrations
release: python manage.py migrate
web: gunicorn cosmiq.wsgi