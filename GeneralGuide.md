# Create django project

## Virtual Environment

```
    virtualenv -v env
```

## Install packages
```
    pip3 install django # for django
    pip3 instal djangorestframework # for REST api
```
## Create Project

```
    django-admin startproject <project name>
```

### Create app

```
    python3 manage.py startapp <app name>
```
Note: Use manage.py although you can use django-admin to startapp (still use manage.py as that way you will not make a mistake to first create project than app)
# Update `settings.py`

Add name of app(shell) and rest_framework to INSTALLED_APPS in the root(project directory)

# Models for app

Next step is to make model for the app in `models.py` inside the app we just created using startapp
After making the models we should make migrations and migrate

```
python3 manage.py makemigrations

python3 manage.py migrate
```
# Serializer for the model

Create `serializers.py` in the app directory and add a serializer model using ModelSerializer

# Views for models

In `views.py` use rest_framework.generics APIviews to create view for the api

# URL for the app

## Create file `urls.py` in shell app
take reference from `urls.py` in the project directory to make the `urls.py` in the app

## Link app urls with project urls
include app urls in api route of project

# Run server
```
python3 manage.py runserver
```






