# Setup

## Virtual Environment
Do this outside the project directory

```
    virtualenv -v env
```

## Install packages
```
    pip3 install django # for django
    pip3 instal djangorestframework # for REST api
```

## Start server

```
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```

