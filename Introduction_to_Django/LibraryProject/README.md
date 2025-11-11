# LibraryProject

This is the initial Django project for the Introduction_to_Django exercises.

Quick start
1. Create and activate a virtual environment (recommended)
   - macOS / Linux:
     ```bash
     python3 -m venv env
     source env/bin/activate
     ```
   - Windows (PowerShell):
     ```powershell
     python -m venv env
     .\env\Scripts\Activate.ps1
     ```
   - Windows (cmd):
     ```cmd
     python -m venv env
     .\env\Scripts\activate.bat
     ```

2. Install dependencies
   ```bash
   pip install --upgrade pip
   pip install django
   ```

3. Verify Django
   ```bash
   python -m django --version
   ```

4. Run the development server
   ```bash
   cd LibraryProject
   python manage.py runserver
   ```
   Open: http://127.0.0.1:8000/

Project structure (created by `django-admin startproject LibraryProject`)

- LibraryProject/
  - manage.py
    - A command-line utility that lets you interact with this Django project.
    - Use `python manage.py runserver`, `migrate`, `createsuperuser`, etc.
  - LibraryProject/ (inner package)
    - __init__.py
      - Marks this directory as a Python package.
    - settings.py
      - Main configuration for this Django project (databases, installed apps, middleware, templates, static files, secret key, debug mode, allowed hosts, etc.)
      - Important: Do not commit SECRET_KEY to public repos—use environment variables for secrets in real projects.
    - urls.py
      - The URL declarations for the project. Acts like a table of contents; includes routing to app-level urls.
      - Default contains a route to the admin and may point the root URL to a default view.
    - asgi.py
      - Entry point for ASGI-compatible web servers to serve your project (async support).
    - wsgi.py
      - Entry point for WSGI-compatible web servers (production deployments using WSGI).

Next recommended steps
- Explore settings.py:
  - Look at INSTALLED_APPS, DATABASES (defaults to sqlite3), DEBUG, ALLOWED_HOSTS, STATIC_URL.
- Look at urls.py:
  - See how the root `urlpatterns` is set up and how you’ll include app-specific urls in the future.
- Create an app:
  - `python manage.py startapp books` (example app name)
  - Register the app in settings.py under INSTALLED_APPS.
- Run migrations and create a superuser:
  - `python manage.py migrate`
  - `python manage.py createsuperuser`
  - Visit http://127.0.0.1:8000/admin/ to log in with the superuser account.

Troubleshooting
- "Address already in use" when running runserver: change port `python manage.py runserver 8001`.
- If `django-admin` is not found: ensure your virtual environment is activated or run `python -m django` to verify installation.
- If DEBUG=False in settings and you see disallowed host: set ALLOWED_HOSTS or use DEBUG=True during development (not for production).

Useful commands reference
- Run shell: `python manage.py shell`
- Make migrations: `python manage.py makemigrations`
- Apply migrations: `python manage.py migrate`
- Create app: `python manage.py startapp <appname>`
- Run tests: `python manage.py test`
- Create superuser: `python manage.py createsuperuser`

License / Notes
- This project was created for learning and demonstration purposes. Do not expose secret keys or production credentials in this repository.