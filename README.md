# django_restaurant"

STEPS:

1. install python3

2. install and activate virtualenv

3. install requred libraries by "pip3 install -r requirements.cfg" in cmd line

4. change directory to where manage.py is then:

     python3 manage.py makemigrations
     
     python3 manage.py migrate
     
     python3 manage.py runserver

7. populate initial data by:

     python3 manage.py shell
     
     from restaurant.fixtures.populate import populate
     
     populate()

8. view project at http://localhost:8000

admin acct is admin:admin