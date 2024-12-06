# AmberPDF

Una librería que procesa un PDF mixto (texto e imágenes/tablas) y extrae el contenido en orden.

## Instalacion

pip install amberpdf

## Uso

import amberpdf

# Configura las credenciales de AWS
amberpdf.credentials('tu_access_key_id', 'tu_secret_access_key')

# Procesa un PDF
text = amberpdf.process_pdf('ruta/al/archivo.pdf', pages = 0)   #"pages" es el número de páginas que analizará, inicia desde la primera página

print(text)
