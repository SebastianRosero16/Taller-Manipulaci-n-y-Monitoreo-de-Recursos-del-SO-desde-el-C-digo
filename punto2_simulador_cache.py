"""
Punto 2 - Simulador de Memoria Caché (L1/L2 vs RAM)
=====================================================
Concepto: Jerarquía de memoria y optimización.

Simula cómo el SO evita acceder al disco constantemente usando
una caché en RAM (un diccionario Python actúa como la caché L2).

- Primera lectura  → va al DISCO (lento, simula RAM → disco)
- Lecturas siguientes → va a la CACHÉ en RAM (rápido, simula L1/L2)

El reto: medir y comparar el tiempo de ambas operaciones.
"""

import time
import os

# ── Caché en memoria (simula jerarquía L1/L2) ─────────────────
# Clave   = ruta del archivo
# Valor   = contenido del archivo en RAM
cache: dict[str, str] = {}
# ──────────────────────────────────────────────────────────────


def leer_archivo(ruta: str) -> tuple[str, str, float]:
    """
    Lee un archivo. Si está en caché lo devuelve desde RAM.
    Si no, lo lee desde disco y lo almacena en caché.

    Retorna: (contenido, origen, tiempo_segundos)
    """
    inicio = time.time()   # <-- inicio del cronómetro

    if ruta in cache:
        contenido = cache[ruta]   # ✅ HIT: lectura desde caché (RAM)
        origen    = "CACHÉ (RAM)"
    else:
        with open(ruta, "r", encoding="utf-8") as archivo:
            contenido = archivo.read()   # ❌ MISS: lectura desde disco
        cache[ruta] = contenido          # guardar en caché para la próxima vez
        origen = "DISCO"

    fin    = time.time()   # <-- fin del cronómetro
    tiempo = fin - inicio

    return contenido, origen, tiempo


def mostrar_resultado(origen: str, tiempo: float, num_chars: int) -> None:
    """Imprime los resultados de una lectura."""
    print(f"  Origen  : {origen}")
    print(f"  Tiempo  : {tiempo:.6f} segundos  ({tiempo * 1000:.3f} ms)")
    print(f"  Tamaño  : {num_chars:,} caracteres leídos")


def comparar_lecturas(ruta: str, repeticiones: int = 3) -> None:
    """Realiza múltiples lecturas y muestra la comparación de tiempos."""
    print(f"\n{'='*55}")
    print(f"  Archivo: {os.path.basename(ruta)}")
    print(f"  Tamaño : {os.path.getsize(ruta) / (1024*1024):.2f} MB")
    print(f"{'='*55}")

    tiempos_disco = []
    tiempos_cache = []

    for i in range(repeticiones + 1):
        print(f"\n  --- Lectura #{i+1} ---")

        # Limpiar caché para la primera lectura (simula arranque en frío)
        if i == 0:
            cache.clear()
            print("  (caché vacía → irá al disco)")

        contenido, origen, tiempo = leer_archivo(ruta)
        mostrar_resultado(origen, tiempo, len(contenido))

        if origen == "DISCO":
            tiempos_disco.append(tiempo)
        else:
            tiempos_cache.append(tiempo)

    # ── Resumen comparativo ────────────────────────────────────
    print(f"\n{'='*55}")
    print("  RESUMEN COMPARATIVO")
    print(f"{'='*55}")

    if tiempos_disco and tiempos_cache:
        promedio_disco = sum(tiempos_disco) / len(tiempos_disco)
        promedio_cache = sum(tiempos_cache) / len(tiempos_cache)
        aceleracion    = promedio_disco / promedio_cache if promedio_cache > 0 else float("inf")

        print(f"  Tiempo promedio desde DISCO : {promedio_disco*1000:.3f} ms")
        print(f"  Tiempo promedio desde CACHÉ : {promedio_cache*1000:.3f} ms")
        print(f"  La caché fue {aceleracion:.1f}x más rápida que el disco")
        print(f"\n  → Esto simula por qué el SO mantiene datos en RAM")
        print(f"    (L1/L2 caché) antes de volver a leer del disco duro.")
    print(f"{'='*55}\n")


def main() -> None:
    print("╔══════════════════════════════════════════════════╗")
    print("║    Simulador de Memoria Caché  (L1/L2 vs RAM)   ║")
    print("╚══════════════════════════════════════════════════╝")

    # Archivo de prueba (genéralo con generar_archivo_grande.py)
    archivo_prueba = "archivo_grande.txt"

    if not os.path.exists(archivo_prueba):
        print(f"\n⚠  No se encontró '{archivo_prueba}'.")
        print("   Ejecuta primero: py -3.11 generar_archivo_grande.py\n")
        return

    # Comparar lecturas: 1 desde disco + 3 desde caché
    comparar_lecturas(archivo_prueba, repeticiones=3)

    # Demostración con múltiples archivos en caché
    print("\n── Demostración: múltiples archivos en caché ──────")
    print(f"  Archivos actualmente en caché: {len(cache)}")
    for ruta_en_cache in cache:
        tam = len(cache[ruta_en_cache]) / (1024 * 1024)
        print(f"    • {os.path.basename(ruta_en_cache)}  ({tam:.2f} MB en RAM)")


if __name__ == "__main__":
    main()
