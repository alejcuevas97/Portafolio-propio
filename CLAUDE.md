# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Personal portfolio site built with **Django 6.0**. Server-rendered pages (Django templates + Tailwind) plus a small read-only REST API (Django REST Framework). Two content apps — `porfolio` (projects) and `certificado` (certifications) — are edited through the Django admin at `/config/`. Deployed on Render (`https://portafolio-propio.onrender.com`); media is stored on Cloudinary.

## Commands

Use the project virtualenv: `.venv/Scripts/python.exe` on Windows (there is also a stale `.venv-1`).

No Node / front-end build — CSS is hand-authored (`static/css/site.css`).

```bash
pip install -r requirements.txt

python manage.py migrate
python manage.py runserver                # http://localhost:8000
python manage.py createsuperuser
python manage.py create_admin             # superuser from DJANGO_SUPERUSER_* env vars; no-ops if unset
python manage.py collectstatic --noinput

python manage.py test                     # Django test runner (tests.py files are empty stubs)
python manage.py test porfolio.tests.SomeTestCase.test_method

bash build.sh                             # Render build: pip + collectstatic + migrate + create_admin
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

**Front-end / design system** — there is **no build step and no Tailwind**. `static/css/site.css` is a hand-authored stylesheet (design direction: "editorial técnico" — restrained saturation, paper-warm neutrals, one muted blue accent, IBM Plex Sans/Mono + Newsreader from Google Fonts, subtle grain via `body::before`). Templates use **semantic class names** defined there (`.wrap`, `.page`, `.hero`, `.eyebrow`, `.section-head`, `.card`, `.card-grid`, `.btn`/`.btn-ghost`, `.entry`/`.entries`, `.defs`/`.def`, `.tags`/`.tag`, `.channels`/`.channel`, `.split`, `.avatar`). Add or extend rules in `site.css`; don't reach for utility classes. Icons are unicode glyphs, not an icon font.

`base.html` is the skeleton: theme pre-paint script → Google Fonts + `site.css` → `{% block chrome %}` (`navbar.html`) → `<main>{% block content %}` → footer → theme-toggle + mobile-nav scripts. `navbar.html` marks the active link via `request.resolver_match.url_name` → `aria-current="page"`.

**Dark mode**: three states via `data-theme` on `<html>` — unset = follow `prefers-color-scheme`; `"light"`/`"dark"` = explicit. `window.toggleTheme()` (in `base.html`) flips and persists to `localStorage.theme`; a pre-paint inline script applies it. All colors are CSS custom properties redefined in three token blocks in `site.css` (`:root`, `@media (prefers-color-scheme: dark) :root:not([data-theme="light"])`, `:root[data-theme="dark"]`) — never hard-code a color outside those blocks.

**i18n**: cookie-based `set_language` + `{% if request.LANGUAGE_CODE == 'es' %}…{% else %}…{% endif %}` branches inline in templates (no `.po`/`.mo` catalogs; `locale/` exists for future `makemessages`).

**CV download**: `index.html`, `perfil.html`, `about.html`, `resume.html` link to `{% static 'cv/CV_Alejandro_Cuevas_Gonzalez.pdf' %}` with `download`. The PDF must be placed at `static/cv/CV_Alejandro_Cuevas_Gonzalez.pdf` (see `static/cv/README.txt`, and `static/cv/cv.html` is a print-to-PDF source) and picked up by `collectstatic`.

**Page purposes** — kept deliberately non-overlapping:
- `/` — marketing hero (pitch + `.spec` panel) + featured PatinPay + a short "Enfoque" skills teaser.
- `/perfil/` — **the person**: photo, first-person bio prose, quick-facts aside. No skills grid, no timeline.
- `/about/` — **the record**: positioning line + canonical skills `defs` + canonical experience timeline (full bullets) + education/certs. This is the source of truth for skills/experience.
- `/resume/` — **the CV hub**: one summary paragraph + Download-PDF/Print buttons + an "at a glance" facts `defs` + a card pointing back to `/about/` and `/proyectos/`. Deliberately does *not* repeat the timeline or skills grid.
- `/proyectos/` — hard-coded featured PatinPay card + DB-driven grid. `/certificaciones/` — DB-driven list.

PatinPay is **not** a DB row — hard-coded on `/` and `/proyectos/`. When editing bio/summary copy, keep the split: personal narrative lives only in `/perfil/`, the structured record only in `/about/`, the condensed CV blurb only in `/resume/`.

## Agent skills

`skills-lock.json` / `.agents/skills/` vendor `supabase-postgres-best-practices` — relevant when working on the Postgres/Supabase database.
