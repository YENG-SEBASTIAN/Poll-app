# mPedigree
mPedigree assessment test

steps to run the poll app

1. clone the Poll project from github
2. create a virtualenv with the command python -m vertualenv (name of your venv)
3. activate the virtualenv with the command ((name of your venv)/scripts/activate)
4. change directory to pollProject (cd pollProject)
5. install the dependances with the command (pip install -r requirements.txt)
6. configure the database in the settings.py file to suit your localhost database
7. make migration to create your database table (python manage.py makemigration)
8. now, run migrate (python manage.py migrate)
9. create a superuser to access the admin panel
10. start your server (python manage.py runserver)
11. open your browser type "http://localhost:8000" or "http://127.0.0.1:8000" 

this time around the application should be up and running