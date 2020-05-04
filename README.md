# django_restaurant"

STEPS:

1. install python3
2. install and activate virtualenv
3. install requirements.cfg
4. python manage.py makemigrations
5. python manage.py migrate
6. python manage.py runserver
7. populate initial data:
    python manage.py shell
    from restaurant.fixtures.populate import populate
    populate()
