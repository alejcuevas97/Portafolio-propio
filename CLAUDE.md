# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Personal portfolio site built with **Django 6.0**. Server-rendered pages (Django templates + Tailwind) plus a small read-only REST API (Django REST Framework). Two content apps — `porfolio` (projects) and `certificado` (certifications) — are edited through the Django admin at `/config/`. Deployed on Render (`https://portafolio-propio.onrender.com`); media is stored on Cloudinary.

## Commands

Use the project virtualenv: `.venv/Scripts/python.exe` on Windows (there is also a stale `.venv-1`).

```bash
pip install -r requirements.txt
npm install
npm run build:css                         # compile static/css/output.css (Tailwind v4 CLI)
npm run watch:css                         # rebuild CSS on change during development

python manage.py migrate
python manage.py runserver                # http://localhost:8000
python manage.py createsuperuser
python manage.py create_admin             # superuser from DJANGO_SUPERUSER_* env vars; no-ops if unset
python manage.py collectstatic --noinput

python manage.py test                     # Django test runner (tests.py files are empty stubs)
python manage.py test porfolio.tests.SomeTestCase.test_method

bash build.sh                             # Render build: pip + npm + collectstatic + migrate + create_admin
```

## Configuration

All deployment values come from the environment, read from a `.env` at the **repo root** (see `.env.example`). `Portafolio/settings.py` also falls back to `Portafolio/.env` for older checkouts.

- **No `DATABASE_URL` → local SQLite** (`db.sqlite3`). Set `DATABASE_URL` (+ optional `DATABASE_REQUIRE_SSL`) for Postgres. The production DB is a Supabase project that is often **paused** — resume it in the Supabase dashboard before running anything that hits it.
- **No Cloudinary credentials → media falls back to local `FileSystemStorage`.** Note: `Project.image` is a `CloudinaryField`, so rendering existing project rows that hold Cloudinary public IDs still needs `CLOUDINARY_*` set — otherwise `/proyectos/` raises "Must supply cloud_name". The API serializer degrades gracefully (returns the public ID string).
- `DEBUG` gates `django_browser_reload` (app + middleware + `/__reload__/` URL) and turns on a block of SSL/cookie hardening when off.
- `ALLOWED_HOSTS` / `CSRF_TRUSTED_ORIGINS` are env lists with sensible `localhost` + `.onrender.com` defaults.

## Architecture

The codebase is written to demonstrate SOLID principles, so there is more indirection than a site this size needs.

**Apps**
- `Portafolio/` — project package: `settings.py`, `urls.py` (root URLconf), `views.py` (static-page class views), `serializers.py`, `api.py` (DRF viewsets), `api_urls.py` (DRF router).
- `porfolio/` — projects app (note the misspelling; the project package is `Portafolio`). `Project` model with Cloudinary image, `ProjectListView`, admin, `ProjectForm`, and `services.ProjectService`.
- `certificado/` — certifications app: `Certification` model, `CertificationListView`, admin, own `urls.py`.

**Routing** (`Portafolio/urls.py`): `/` `/about/` `/perfil/` `/resume/` `/contact/` are template pages; `/set-language/<code>/`; `/proyectos/`; `/certificaciones/` (included from `certificado.urls`); `/config/` admin; `/api/` (see below).

**REST API** (`/api/`, `Portafolio/api.py` + `api_urls.py`): read-only `ReadOnlyModelViewSet`s for projects and certifications via a `DefaultRouter` (`/api/projects/`, `/api/certifications/`), plus SimpleJWT token endpoints (`/api/auth/token/`, `/api/auth/token/refresh/`). Default permission is `IsAuthenticatedOrReadOnly`; page size 12. Serializers live in `Portafolio/serializers.py`; `ProjectSerializer.image` is a `SerializerMethodField` that returns `.url` or falls back to the raw public ID.

**Static pages** (`Portafolio/views.py`): all extend `BasePageView` (a `TemplateView` adding `page_title` to context); each page view just sets `template_name` + `page_title`.

**Projects business logic**: `porfolio/services.py` `ProjectService` (static methods: list, count, search, cached list, CRUD, by-year) is the single service layer. `ProjectListView` calls `ProjectService.get_all_projects()`. Model-level validation is in `ProjectValidator`, invoked from `Project.save()`. Form-level checks (min lengths) are in `ProjectForm.clean()`.

**Templates** (`templates/`): `base.html` is the skeleton — it loads the compiled Tailwind (`{% static 'css/output.css' %}`) and Font Awesome (cdnjs stylesheet) once, then includes `navbar.html` inside `<body>`. Page templates extend `base.html`. Some templates still contain stray `<head>`/`<body>` tags inside their content block — invalid nesting that browsers tolerate; tidy opportunistically, don't rewrite wholesale. `index.html` blanks the navbar block. i18n uses cookie-based `set_language` + `{% if request.LANGUAGE_CODE == 'es' %}` branches in templates; there are no `.mo` catalogs yet (`locale/` exists for future `makemessages`).

**CV download**: `perfil.html`, `about.html` and `resume.html` link to `{% static 'cv/CV_Alejandro_Cuevas_Gonzalez.pdf' %}` with a `download` attribute. The PDF must be placed at `static/cv/CV_Alejandro_Cuevas_Gonzalez.pdf` (see `static/cv/README.txt`) and picked up by `collectstatic`.

**Tailwind**: `src/input.css` = `@import "tailwindcss";` + `@source "../templates";` + a **dark-mode override block**. `npm run build:css` compiles `static/css/output.css` (git-ignored, rebuilt in `build.sh` before `collectstatic`). Re-run it after adding new utility classes to templates. No CDN is used at runtime.

**Dark mode**: toggled by a `.dark` class on `<html>`, persisted to `localStorage.theme`, applied before first paint by an inline script in `base.html` (falls back to `prefers-color-scheme`). `window.toggleTheme()` + the sun/moon button (`[data-theme-icon]`) live in `base.html`/`navbar.html`. Templates use plain color utilities (no `dark:` variants); instead the `.dark …` rules at the end of `src/input.css` remap the specific `bg-*`/`text-*`/`border-*` utilities in use. When a template introduces a new color utility, add it to that block and rebuild.

## Agent skills

`skills-lock.json` / `.agents/skills/` vendor `supabase-postgres-best-practices` — relevant when working on the Postgres/Supabase database.
