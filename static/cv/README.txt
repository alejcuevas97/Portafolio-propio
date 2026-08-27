CV
==

cv.html   -> versión maquetada del CV, lista para imprimir (SIEMPRE la fuente de verdad).
CV_Alejandro_Cuevas_Gonzalez.pdf  -> el PDF que descargan los botones "Descargar CV".

Para regenerar el PDF tras cambiar cv.html:
  1. Abre static/cv/cv.html en el navegador (doble clic).
  2. Ctrl+P  ->  Destino: "Guardar como PDF"  ->  desactiva encabezados/pies.
  3. Guárdalo AQUÍ con el nombre EXACTO (el navegador suele proponer otro):

         CV_Alejandro_Cuevas_Gonzalez.pdf   (con guiones bajos, sin acentos)

     Si te lo guarda como "CV — Alejandro Cuevas González.pdf", renómbralo.
  4. python manage.py collectstatic --noinput --clear
  5. En el navegador, recarga con Ctrl+Shift+R (el PDF viejo queda en caché).
