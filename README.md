# OpenSaaS

A Django-based SaaS platform for managing organizations and deploying services on [Railway](https://railway.app). The app supports superuser-only login, organization management, and automated deployment of services (including Postgres) via the Railway API.

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

Railway integration uses credentials stored in the database (Django admin).

1. Start the development server:
   ```bash
   python manage.py runserver
   ```
2. Open the admin: **http://127.0.0.1:8000/admin/**
3. Log in with your superuser account.
4. Under **Admin app** → **Creadentials**, click **Add Creadentials** (or edit the existing one).
5. Fill in:

   | Field                  | Description |
   |------------------------|-------------|
   | **Railway auth token** | Your [Railway API token](https://railway.app/account/tokens). Used to authenticate GraphQL requests. |
   | **Railway workspace id** | The workspace ID where projects will be created. Find it in the Railway dashboard URL or via API. |
   | **Raiway template id** | Template ID used for `templateDeployV2` deployments. Get this from your Railway template or dashboard. |

6. Save. The app uses the **first** credentials record for all Railway API calls.

**Where to get these values:**

- **Auth token:** [Railway → Account → Tokens](https://railway.app/account/tokens) → Create token.
- **Workspace ID:** In Railway, open your team/workspace; the ID often appears in the URL or in project/workspace settings.
- **Template ID:** From the template you want to use for deployments (e.g. in the template’s URL or API response).

### 7. Run the app

```bash
python manage.py runserver
```

- **App (login):** http://127.0.0.1:8000/  
- **Login page:** http://127.0.0.1:8000/user/login/  
- **Django admin:** http://127.0.0.1:8000/admin/

---

## Optional: environment variables

The project uses `python-dotenv` and loads a `.env` file from the project root if present. You can use it for local overrides (e.g. `DEBUG`, `SECRET_KEY`). For production, set variables in your hosting environment and avoid committing `.env` with secrets.

---

## Project structure

| Path              | Description |
|-------------------|-------------|
| `opensaas/`       | Django project settings and root URL config. |
| `admin_app/`      | Credentials model and admin for Railway auth/template/workspace. |
| `organization/`   | Organizations, projects, services, Railway API (`railway.py`), and deployment logic. |
| `user_management/`| Superuser login and auth views. |
| `templates/`      | Shared templates (login, modals, list/detail views). |

---

## Security notes

- **Production:** Set `DEBUG = False`, use a strong `SECRET_KEY`, and configure `ALLOWED_HOSTS` in `opensaas/settings.py`.
- **Railway token:** Keep your Railway auth token secret; it has full access to your Railway account.
- **Superuser:** Only create superusers for trusted admins; they can access Django admin and all app features.

---

## License

Use and modify as needed for your project.
