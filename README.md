# KinoCMS

Website and content management system for a cinema network: movies, cinemas, halls, showtimes and **real-time seat booking over WebSockets**, with a custom admin panel and bilingual (UA/EN) content.

> **Demo:** TODO — add a live demo link (or remove this line)
>
> **Screenshots:** TODO — add screenshots of the seat booking page, schedule and admin dashboard (e.g. `docs/screenshots/*.png`)

## Features

**Public website**
- Home page with banners, "now showing" and "coming soon" posters
- Showtime schedule with filtering by cinema, hall and date
- **Live seat booking** — Django Channels consumer (`ws/booking/<schedule_id>/`) broadcasts seat reservations, cancellations and purchases to everyone viewing the same showtime
- Cinemas, halls, contacts, news and promotions, custom content pages
- Registration, login and profile editing
- Ukrainian / English UI and content (Django i18n + `django-modeltranslation`)

**Admin panel (`/adminlte/`, superuser only)**
- Dashboard with charts: users by gender, sessions for the last 7 days, traffic sources
- CRUD for movies, cinemas, halls, showtimes, news & promotions, pages, contacts
- Banner and slider management (top, news, background banners)
- User management
- **Email campaigns**: upload an HTML template and send it to all or selected users via a **Celery** task (Redis broker)

**Management commands**
- `init_pages` — creates the mandatory static pages, main page and contacts singletons
- `init_schedule` — generates showtimes for every hall/movie within the movie's showing period

## Tech stack

- Python 3.12, Django 5.2
- Django Channels + Daphne (ASGI), channels-redis
- Celery + Redis
- PostgreSQL 15
- django-modeltranslation, python-decouple, Pillow
- Gunicorn, Nginx (HTTP + WebSocket proxy), Docker / Docker Compose
- Frontend: Django templates, Bootstrap, AdminLTE, Chart.js

## Project structure

```
config/          settings, URLs (i18n patterns), ASGI routing, Celery app
src/
  main/          public pages, schedule, booking, WebSocket consumer, management commands
  cms/           movies, cinemas, halls, banners, contacts, SEO, mailing models
  core/adminlte/ custom admin panel views and the Celery mailing task
  authentication/ login, registration, profile
  user/          custom User model
templates/       base layouts
locale/          translations
deploy/          Dockerfiles (backend, nginx, db), Nginx config, entrypoint
```

## Running locally (Docker Compose)

1. Create `local.env` in the project root (git-ignored):

   ```env
   SECRET_KEY=change-me
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1

   DB_NAME=kinocms
   DB_USER=kinocms
   DB_PASSWORD=kinocms
   DB_HOST=db
   DB_PORT=5432
   POSTGRES_DB=kinocms
   POSTGRES_USER=kinocms
   POSTGRES_PASSWORD=kinocms

   REDIS_HOST=redis
   REDIS_PORT=6379

   EMAIL_HOST_USER=you@gmail.com
   EMAIL_HOST_PASSWORD=app-password
   ```

2. Start the stack (`docker-compose.yml` + `docker-compose.override.yml` are picked up automatically; the override runs Django's dev server on port 8000):

   ```bash
   docker compose up -d --build
   docker compose exec backend python manage.py migrate
   docker compose exec backend python manage.py createsuperuser
   docker compose exec backend python manage.py init_pages
   ```

3. Open http://localhost:8000/ (dev server) or http://localhost/ (Nginx, which also proxies `/ws/` to the Daphne `channels` service). Admin panel: `/uk/adminlte/` or `/en/adminlte/`.

4. Email campaigns need a Celery worker (not defined as a separate Compose service yet):

   ```bash
   docker compose exec backend celery -A config worker -l info
   ```

To mount the full project directory for live code reload, add the dev overlay:

```bash
docker compose -f docker-compose.yml -f docker-compose.override.yml -f docker-compose.dev.yml up --build
```

### Production

`docker-compose.prod.yml` reads variables from `.env`; the base compose file runs `collectstatic`, `migrate` and Gunicorn behind Nginx:

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

## TODO

- [ ] Screenshots / demo link
- [ ] Add a `celery` worker service to Compose
- [ ] Add a `local.env.example`
- [ ] Automated tests
