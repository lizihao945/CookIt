# CookIt

## Python Environment Setup

```
mkvirtualenv --python=$(which python3) cookit
pip install -r requirements.txt

# Next time
workon cookit
```

## Bootstrap Script
```
django-admin startproject CookIt
python manage.py startapp recipes
```
