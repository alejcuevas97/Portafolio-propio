# Perfil de GitHub — estado y mantenimiento

El README del perfil vive en el repo público **`alejcuevas97/alejcuevas97`**
(GitHub lo muestra arriba de `github.com/alejcuevas97` por llamarse igual que el usuario).

**Ya está publicado y funcionando.** Esta carpeta (`perfil-github/`) es la copia de
trabajo desde la que editamos.

```
perfil-github/
├── README.md                     ← copia de lo que hay en el repo del perfil
└── .github/workflows/
    ├── snake.yml                 ← genera la animación de la serpiente (rama output)
    └── metrics.yml               ← genera metrics.svg en la rama main
```

## Qué compone el README

| Bloque | De dónde sale | Fiabilidad |
| --- | --- | --- |
| **Cabecera animada** (texto que se escribe solo) | servicio `readme-typing-svg.demolab.com`, configurado en la URL del `<img>` del README | servicio gratuito, estable |
| Badges (Portafolio, PatinPay, LinkedIn, Email, visitas) | `shields.io` + `komarev.com` | estables |
| Iconos del stack | `skillicons.dev` | estable |
| **`metrics.svg`** (actividad, lenguajes, calendario) | Action `lowlighter/metrics` → se guarda en la rama `main` del repo | **siempre carga** (archivo propio) |
| **Serpiente** | Action `Platane/snk` → se guarda en la rama `output` | **siempre carga** (archivo propio) |

> La foto ya no va en el banner: se ve en el avatar del perfil.
> Las tarjetas de `github-readme-stats` / `streak` / `trophy` se descartaron porque
> fallan por saturación; `metrics.svg` las sustituye y es un archivo del propio repo.

## Configuración del repo (ya hecha)

- **Settings → Actions → General → Workflow permissions → "Read and write permissions".**
  Imprescindible para que los workflows escriban `metrics.svg` y la rama `output`.
- `metrics.yml` usa `secrets.METRICS_TOKEN || secrets.GITHUB_TOKEN`, así que funciona
  con el token automático. Solo hace falta crear el secret `METRICS_TOKEN` (PAT classic
  con scope `repo`) **si** se quieren contar también los repos privados.

Los workflows se re-ejecutan solos: `metrics.yml` una vez al día, `snake.yml` cada 12 h,
y ambos en cada push a `main`. También a mano desde la pestaña **Actions → Run workflow**.

## Cómo editar

- **Frases del texto animado:** en `README.md`, parámetro `lines=` de la URL del
  primer `<img>` (frases separadas por `;`, caracteres codificados para URL).
  Color: `color=2563EB` (el azul del portafolio).
- **Stack:** lista `i=` en las URLs de `skillicons.dev` ([opciones](https://skillicons.dev)).
- **Métricas:** añade/quita `plugin_*` en `metrics.yml`
  ([docs](https://github.com/lowlighter/metrics)).

Tras editar `README.md` aquí, súbelo al repo del perfil (arrástralo con *Upload files*
o `git push`). No uses "Create new file" + pegar para archivos con líneas muy largas.
