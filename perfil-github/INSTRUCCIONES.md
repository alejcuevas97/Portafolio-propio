# Cómo publicar tu README de perfil

GitHub muestra un README especial arriba de tu perfil (`github.com/alejcuevas97`)
cuando existe un repo **público** cuyo nombre es **igual a tu usuario**.

## Qué contiene esta carpeta

```
perfil-github/
├── README.md                     ← va a la raíz del repo del perfil
├── assets/
│   ├── header.svg                ← banner (tu foto va incrustada dentro; único archivo necesario)
│   └── avatar.png                ← solo la fuente de la foto, por si regeneras el banner
└── .github/workflows/
    ├── snake.yml                 ← genera la animación de la serpiente
    └── metrics.yml               ← genera metrics.svg (estadísticas)
```

El diseño está **ligado al portafolio**: mismo azul (`#2563EB`), tarjeta blanca con
borde gris, foto con anillo azul y punto verde, y el sello "Portfolio" del navbar.

Todo lo que se ve en el README es **fiable**:
- El **banner** (`header.svg`, con tu foto incrustada en base64) y las **métricas**
  (`metrics.svg`) son archivos guardados **dentro de tu propio repo**, así que
  **siempre cargan** — a diferencia de las tarjetas de `vercel.app` que fallan por
  saturación (por eso las quitamos).
- Los iconos del stack usan `skillicons.dev` y los badges `shields.io`, ambos estables.

---

## 1. Crear el repo y subir los archivos

### Opción A — Web (sin Git)

1. Crea un repo **público** llamado **`alejcuevas97`**. Marca *"Add a README file"*.
2. **Subir el README:** abre `README.md` en el repo → lápiz ✏️ → pega el contenido
   de [`README.md`](./README.md) → *Commit changes*.
3. **Subir el banner:** botón *Add file → Upload files* → arrastra
   `assets/header.svg` (súbelo tal cual: pesa ~55 KB porque lleva tu foto dentro).
   Si prefieres *Create new file*, ponle nombre `assets/header.svg` y pega el
   contenido. `avatar.png` no hace falta subirlo.
4. **Subir los workflows:** repite *Add file → Create new file* dos veces:
   - `.github/workflows/snake.yml`  → contenido de [`snake.yml`](./.github/workflows/snake.yml)
   - `.github/workflows/metrics.yml` → contenido de [`metrics.yml`](./.github/workflows/metrics.yml)

### Opción B — Git

```bash
git clone https://github.com/alejcuevas97/alejcuevas97.git
cd alejcuevas97
cp -r "<ruta>/perfil-github/README.md" "<ruta>/perfil-github/assets" "<ruta>/perfil-github/.github" .
git add .
git commit -m "Perfil: README + banner + workflows"
git push origin main
```

---

## 2. Permisos de las Actions (obligatorio, una sola vez)

Repo → **Settings** → **Actions** → **General** → abajo, **"Workflow permissions"**
→ marca **"Read and write permissions"** → **Save**.

---

## 3. Token para las métricas (`metrics.yml`)

El workflow de métricas necesita un token personal:

1. Ve a <https://github.com/settings/tokens> → **Generate new token** → **classic**.
2. Nombre: `metrics`. Expiración: la que quieras (p. ej. 90 días o *No expiration*).
3. Scopes (casillas):
   - Solo repos públicos → **no marques nada**.
   - Quieres contar también repos privados → marca **`repo`**.
4. **Generate token** y **copia** el valor (empieza por `ghp_...`).
5. En tu repo del perfil: **Settings** → **Secrets and variables** → **Actions**
   → **New repository secret**:
   - Name: `METRICS_TOKEN`
   - Secret: pega el token
   → **Add secret**.

> Si no quieres crear el token ahora, borra el archivo `.github/workflows/metrics.yml`
> y la sección de métricas del README; el resto (banner, stack, serpiente, proyectos)
> funciona igual.

---

## 4. Primera ejecución

Cada `push` a `main` dispara los dos workflows. Si ya subiste todo, ve a la
pestaña **Actions** y espera a que **"Metricas de GitHub"** y
**"Generar animación de la serpiente"** tengan el ✅ verde (~1–3 min).

- ❌ en la serpiente → casi siempre es el **paso 2** (permisos). Arréglalo y en
  Actions abre el intento fallido → **Re-run jobs**.
- ❌ en las métricas → revisa que el secret se llame exactamente `METRICS_TOKEN`.

Al terminar existirán:
- `metrics.svg` en la rama `main`
- la rama `output` con `github-snake.svg` y `github-snake-dark.svg`

Hasta que corran por primera vez, esas dos imágenes del README saldrán rotas: es normal.

---

## Personalización

- **Colores del banner:** edita `assets/header.svg` (busca `#2E9EF7`).
- **Frases del banner:** el texto está en `assets/header.svg`, en las etiquetas `<text>`.
- **Iconos del stack:** cambia la lista `i=` en las URLs de `skillicons.dev`
  ([lista completa](https://skillicons.dev)).
- **Contenido de las métricas:** en `metrics.yml` puedes añadir/quitar `plugin_*`
  ([docs de lowlighter/metrics](https://github.com/lowlighter/metrics)).
