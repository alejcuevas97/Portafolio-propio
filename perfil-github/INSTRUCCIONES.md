# Cómo publicar tu README de perfil (estilo MoureDev)

GitHub muestra un README especial en la parte superior de tu perfil
(`github.com/alejcuevas97`) cuando existe un repositorio **público** cuyo
nombre es **exactamente igual a tu nombre de usuario**.

## Pasos

1. Crea un repo nuevo, público, llamado **`alejcuevas97`**
   (mismo nombre que tu usuario). GitHub te mostrará un aviso:
   *"You found a secret! alejcuevas97/alejcuevas97 is a special repository…"*.

2. Marca la opción **"Add a README file"** (o súbelo después).

3. Copia el archivo [`README.md`](./README.md) de esta carpeta a la raíz de ese repo.

4. Commit a la rama `main`. Al abrir tu perfil ya verás la presentación.

## Con línea de comandos

```bash
# en una carpeta aparte, no dentro de este proyecto
git clone https://github.com/alejcuevas97/alejcuevas97.git
cd alejcuevas97

# copia el README y el workflow de la serpiente
cp "<ruta>/perfil-github/README.md" .
cp -r "<ruta>/perfil-github/.github" .

git add README.md .github
git commit -m "Perfil estilo MoureDev + animación snake"
git push origin main
```

## Animación de la serpiente (snake) — pasos extra

El archivo [`.github/workflows/snake.yml`](./.github/workflows/snake.yml) genera
cada 12 h un SVG de una serpiente que "se come" tus contribuciones y lo publica
en una rama `output` del mismo repo. El README ya apunta a esa rama.

1. Sube la carpeta `.github/` al repo `alejcuevas97/alejcuevas97` (ver comandos arriba).
2. En el repo, **Settings → Actions → General → Workflow permissions** →
   marca **"Read and write permissions"** y guarda.
3. Ve a la pestaña **Actions**, elige *"Generar animación de la serpiente"* y
   pulsa **"Run workflow"** una vez para la primera generación.
4. Se creará la rama `output` con `github-snake.svg` y `github-snake-dark.svg`.
   A partir de ahí se actualiza sola.

Mientras la rama `output` no exista, esa imagen del README saldrá rota: es normal
hasta que corras el workflow la primera vez.

## Notas sobre las imágenes dinámicas

Las tarjetas usan servicios públicos gratuitos que se renderizan solos:

| Servicio | Para qué | Nota |
| --- | --- | --- |
| `readme-typing-svg.demolab.com` | Texto animado del encabezado | Edita el parámetro `lines=` para cambiar las frases |
| `img.shields.io` | Badges de tecnologías y sociales | Sin configuración |
| `github-readme-stats.vercel.app` | Tarjetas de stats y lenguajes | Para contar repos privados necesitas desplegar tu propia instancia |
| `streak-stats.demolab.com` | Racha de contribuciones | — |
| `github-profile-trophy.vercel.app` | Trofeos | — |
| `komarev.com/ghpvc` | Contador de visitas | — |

Si algún servicio va lento algún día, es normal (son gratuitos y compartidos).

## Personalización rápida

- **Colores:** cambia `2E9EF7` (azul) y `theme=tokyonight` por otro tema
  (`radical`, `dracula`, `catppuccin_mocha`, `github_dark`…).
- **Animación de la serpiente (snake):** ya incluida en `.github/workflows/snake.yml`
  (ver sección de arriba para activarla).
- **Redes:** añade badges de YouTube, Twitch, Discord o X con el mismo patrón
  `img.shields.io/badge/...`.
