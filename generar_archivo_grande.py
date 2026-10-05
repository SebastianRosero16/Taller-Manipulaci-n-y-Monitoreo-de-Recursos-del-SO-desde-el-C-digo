"""
Script auxiliar: genera un archivo de texto grande (~50 MB)
para usar como dato de prueba en el simulador de caché.
Solo necesitas ejecutarlo una vez.
"""

import os

NOMBRE_ARCHIVO = "archivo_grande.txt"
TAMANO_MB      = 50   # tamaño deseado en MB

linea = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 10 + "\n"
bytes_por_linea = len(linea.encode("utf-8"))
lineas_necesarias = (TAMANO_MB * 1024 * 1024) // bytes_por_linea

print(f"Generando '{NOMBRE_ARCHIVO}' de ~{TAMANO_MB} MB ({lineas_necesarias:,} líneas)...")

with open(NOMBRE_ARCHIVO, "w", encoding="utf-8") as f:
    for i in range(lineas_necesarias):
        f.write(f"[Línea {i+1:08d}] {linea}")

tamanio_real = os.path.getsize(NOMBRE_ARCHIVO) / (1024 * 1024)
print(f"Archivo creado: {tamanio_real:.2f} MB")
