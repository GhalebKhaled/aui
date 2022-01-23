## About the project
AUI assignment, on top of Django

### Part 1:
Handled in `assignment/apis`

### Part 2:
Partially handled in `assignment/management/commands/enrich_tweets.py`
Can we run using

```
./manage.py enrich_tweets http://aui-lab-data-engineer-resources.s3.amazonaws.com/tweets/clubs-tweets.parquet
```

### Part 3:
Not done

### Part 4:
Not done


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



Then run django server

```
python manage.py runserver
```

