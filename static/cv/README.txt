CV
==

cv.html  ->  versión maquetada del CV, lista para imprimir.

Para generar el PDF:
  1. Abre static/cv/cv.html en el navegador (doble clic, o arrástralo a una pestaña).
  2. Pulsa "Imprimir / Guardar como PDF"  (o Ctrl+P).
  3. En "Destino" elige "Guardar como PDF" y desactiva encabezados/pies de página.
  4. Guarda el archivo aquí mismo con el nombre exacto:

         CV_Alejandro_Cuevas_Gonzalez.pdf

  5. python manage.py collectstatic --noinput

Los botones "Descargar CV" de perfil/, about/ y resume/ apuntan a
{% static "cv/CV_Alejandro_Cuevas_Gonzalez.pdf" %}.
