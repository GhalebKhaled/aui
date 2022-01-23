## About the project
AUI assignment

## Setup Steps

```
virtualenv venv

source venv/bin/activate

pip install -r requirements.txt

[Configure env. variables if not working local]


```

## Running the app

If you don't have `local.py` in your settings, copy `settings/local.template.py` to `settings/local.py`
and don't forget to update the keys if missing (like mailgun key)

run redis server using:

```
redis-server
```

Then:

```
run django server

python manage.py runserver
```

