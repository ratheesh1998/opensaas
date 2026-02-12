# OpenSaaS

A Django-based SaaS platform for deploying and managing SaaS instances on [Railway](https://railway.app). Create deployment templates, spin up organizations, and manage environment variables—all from a single dashboard.

## Features

- **Landing page** – Public homepage for new visitors
- **Deployment templates** – Define services and env vars per template
- **Organization management** – Deploy instances from templates
- **Environment variables** – Add, update, and delete per service
- **Superuser-only access** – Secure login for administrators

---

## Requirements

- **Python** 3.10+ (3.14 used in project)
- **pip** (Python package manager)

### Python dependencies

Install from `requirements.txt`:

```bash
pip install -r requirements.txt
```

Included packages:

- **Django** – web framework
- **python-dotenv** – load environment variables from `.env`
- **requests** – HTTP client for Railway API calls

---

## Quick start

### 1. Clone and enter the project

```bash
cd opensaas
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
```

- **Windows (PowerShell):** `.\venv\Scripts\Activate.ps1`
- **Windows (CMD):** `venv\Scripts\activate.bat`
- **macOS/Linux:** `source venv/bin/activate`

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Create a superuser

Only superusers can log in to the app. Create one with:

```bash
python manage.py createsuperuser
```

Enter:

- **Username** (required)
- **Email** (optional; can leave blank)
- **Password** (twice; must meet Django’s validation)

### 6. Add Railway credentials

Railway integration uses credentials stored in the database. You can add them via:

**Option A – Settings modal (recommended)**

1. Start the dev server and open **http://127.0.0.1:8000/**:
   ```bash
   python manage.py runserver
   ```
2. Click **Get Started** and log in
3. Click the **Settings** button in the dashboard navbar
4. Fill in Railway auth token, workspace ID, and template ID
5. Save

**Option B – Django admin:** Open **http://127.0.0.1:8000/admin/**, go to **Admin app** → **Creadentials**. Fill in:

   | Field                  | Description |
   |------------------------|-------------|
   | **Railway auth token** | Your [Railway API token](https://railway.app/account/tokens). Used to authenticate GraphQL requests. |
   | **Railway workspace id** | The workspace ID where projects will be created. Find it in the Railway dashboard URL or via API. |
   | **Raiway template id** | Template ID used for `templateDeployV2` deployments. Get this from your Railway template or dashboard. |

6. Save. The app uses the **first** credentials record for all Railway API calls.

### 7. Run the app

```bash
python manage.py runserver
```

| URL | Description |
|-----|-------------|
| http://127.0.0.1:8000/ | Homepage (landing page) |
| http://127.0.0.1:8000/app/ | Dashboard (requires login) |
| http://127.0.0.1:8000/user/login/ | Sign in |
| http://127.0.0.1:8000/admin_app/settings/template-list/ | Deployment templates |
| http://127.0.0.1:8000/admin/ | Django admin |

---

## Migrations

Migration files are ignored via `.gitignore`. After cloning:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Optional: environment variables

The project uses `python-dotenv` and loads a `.env` file from the project root if present. You can use it for local overrides (e.g. `DEBUG`, `SECRET_KEY`). For production, set variables in your hosting environment and avoid committing `.env` with secrets.

---

## Project structure

| Path               | Description |
|--------------------|-------------|
| `opensaas/`        | Django project settings and root URL config |
| `admin_app/`       | Credentials, deployment templates, services, environment variables |
| `organization/`    | Organizations, projects, Railway API (`railway.py`), deployment logic |
| `user_management/` | Superuser login and auth views |
| `templates/`       | Homepage, login, dashboard, modals, list/detail views |

---

## Security notes

- **Production:** Set `DEBUG = False`, use a strong `SECRET_KEY`, and configure `ALLOWED_HOSTS` in `opensaas/settings.py`.
- **Railway token:** Keep your Railway auth token secret; it has full access to your Railway account.
- **Superuser:** Only create superusers for trusted admins; they can access Django admin and all app features.

---

## License

Use and modify as needed for your project.
