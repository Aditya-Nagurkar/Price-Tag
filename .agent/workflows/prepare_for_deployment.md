---
description: Prepare Django App for Render.com Deployment
---

# Prepare for Render Deployment

This workflow configures the Django application for deployment on Render.com (or similar PaaS like Heroku).

## 1. Install Production Dependencies
We need `gunicorn` for the web server, `whitenoise` for serving static files, and database adapters.

```bash
pip install gunicorn whitenoise dj-database-url psycopg2-binary
pip freeze > requirements.txt
```

## 2. Create build.sh
This script will run on Render to install dependencies, collect static files, and migrate the database.

```bash
#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
```

## 3. Create Procfile
This tells Render how to run the app.

```text
web: gunicorn price_tracker.wsgi
```

## 4. Update settings.py
We need to configure WhiteNoise and database settings.

**Steps to perform manually or via agent:**
1.  Add `whitenoise.middleware.WhiteNoiseMiddleware` to `MIDDLEWARE` in `settings.py` (after `SecurityMiddleware`).
2.  Set `STATIC_ROOT = BASE_DIR / 'staticfiles'`.
3.  Update `DATABASES` to use `dj_database_url` if a `DATABASE_URL` env var is present.
4.  Update `ALLOWED_HOSTS` to accept the Render URL (e.g., `['*']` or specific domains).

## 5. Deployment Steps (User Action)
1.  Push these changes to GitHub.
2.  Go to [Render.com](https://render.com).
3.  Create a new **Web Service**.
4.  Connect your GitHub repository.
5.  Set **Build Command** to `./build.sh`.
6.  Set **Start Command** to `gunicorn price_tracker.wsgi`.
7.  Add Environment Variables:
    *   `PYTHON_VERSION`: `3.11.5` (or your version)
    *   `SECRET_KEY`: (Generate a new random key)
    *   `DEBUG`: `False`
    *   `DATABASE_URL`: (Render provides this if you add a Postgres DB, or use SQLite for testing but warning: data will be lost on restart)
