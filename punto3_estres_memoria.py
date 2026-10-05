"""
Punto 3 - Estrés de Memoria y Salto a la Virtual (Paginación)
==============================================================
Concepto: Memoria Virtual y Archivo de Paginación.

Este script llena progresivamente la RAM con millones de strings
hasta alcanzar un límite de seguridad configurado, forzando al SO
a usar la memoria virtual (swap / archivo de paginación).

ADVERTENCIA: Mientras corre, abre el Administrador de Tareas
(Ctrl+Shift+Esc) → pestaña "Rendimiento" → "Memoria" y observa:
  • "En uso"       → RAM física consumida
  • "Comprometida" → incluye memoria virtual (swap)

Cuando "Comprometida" supera "Total RAM" = el SO activó la paginación.
"""

import psutil
import time
import sys

# ── Límite de seguridad ────────────────────────────────────────
# El script se detiene cuando la RAM usada supere este porcentaje.
# Mantenerlo en 85% para no bloquear la máquina.
LIMITE_RAM_PCT    = 85       # % máximo de RAM física permitido
STRINGS_POR_BLOQUE = 100_000  # strings que se agregan por iteración
TAMANO_STRING      = 1_000    # caracteres por string (~1 KB cada uno)
INTERVALO_REPORTE  = 1        # segundos entre reportes en consola
# ──────────────────────────────────────────────────────────────


def obtener_estado_memoria() -> dict:
    """Retorna el estado actual de RAM y memoria virtual."""
    ram   = psutil.virtual_memory()
    swap  = psutil.swap_memory()
    return {
        "ram_pct"        : ram.percent,
        "ram_usada_gb"   : ram.used       / (1024 ** 3),
        "ram_total_gb"   : ram.total      / (1024 ** 3),
        "ram_disponible" : ram.available  / (1024 ** 3),
        "swap_pct"       : swap.percent,
        "swap_usada_gb"  : swap.used      / (1024 ** 3),
        "swap_total_gb"  : swap.total     / (1024 ** 3),
    }


def mostrar_estado(estado: dict, bloques: int, total_strings: int) -> None:
    """Imprime el estado actual de memoria en consola."""
    ram_barra  = generar_barra(estado["ram_pct"])
    swap_barra = generar_barra(estado["swap_pct"])

    print(f"\n  Bloque #{bloques:,}  |  Strings en memoria: {total_strings:,}")
    print(f"  RAM  : {ram_barra} {estado['ram_pct']:5.1f}%"
          f"  ({estado['ram_usada_gb']:.2f} / {estado['ram_total_gb']:.2f} GB)")
    print(f"  SWAP : {swap_barra} {estado['swap_pct']:5.1f}%"
          f"  ({estado['swap_usada_gb']:.2f} / {estado['swap_total_gb']:.2f} GB)")

    if estado["swap_pct"] > 0:
        print("  *** El SO está usando MEMORIA VIRTUAL (PAGINACIÓN ACTIVA) ***")


def generar_barra(porcentaje: float, largo: int = 20) -> str:
    """Genera una barra de progreso ASCII."""
    llenas = int(min(porcentaje, 100) / 100 * largo)
    return "[" + "█" * llenas + "░" * (largo - llenas) + "]"


def main() -> None:
    print("╔══════════════════════════════════════════════════════╗")
    print("║   Estrés de Memoria  |  Forzando Paginación Virtual  ║")
    print("╚══════════════════════════════════════════════════════╝")

    estado_inicial = obtener_estado_memoria()
    print(f"\n  RAM total del sistema : {estado_inicial['ram_total_gb']:.2f} GB")
    print(f"  RAM en uso al inicio  : {estado_inicial['ram_usada_gb']:.2f} GB"
          f"  ({estado_inicial['ram_pct']:.1f}%)")
    print(f"  Límite de seguridad   : {LIMITE_RAM_PCT}%")
    print(f"\n  ⚠  Abre el Administrador de Tareas ahora (Ctrl+Shift+Esc)")
    print(f"     y observa la pestaña 'Rendimiento' → 'Memoria'")
    print(f"\n  Iniciando en 3 segundos... (Ctrl+C para cancelar)")
    time.sleep(3)

    # ── Contenedor principal: lista de strings en RAM ──────────
    contenedor = []
    bloques    = 0

    print(f"\n{'─'*55}")
    print("  Llenando memoria...")
    print(f"{'─'*55}")

    try:
        while True:
            # Agregar un bloque de strings a la lista
            bloque = ["X" * TAMANO_STRING for _ in range(STRINGS_POR_BLOQUE)]
            contenedor.extend(bloque)
            bloques += 1

            estado = obtener_estado_memoria()

            # Mostrar reporte cada INTERVALO_REPORTE segundos aprox.
            mostrar_estado(estado, bloques, len(contenedor))

            # ── Límite de seguridad ────────────────────────────
            if estado["ram_pct"] >= LIMITE_RAM_PCT:
                print(f"\n{'='*55}")
                print(f"  LÍMITE DE SEGURIDAD ALCANZADO: {estado['ram_pct']:.1f}%")
                print(f"  El script se detiene para proteger el sistema.")
                print(f"{'='*55}")
                break

            time.sleep(INTERVALO_REPORTE)

    except KeyboardInterrupt:
        print("\n\n  Script detenido manualmente por el usuario.")

    # ── Estadísticas finales ───────────────────────────────────
    estado_final = obtener_estado_memoria()
    memoria_consumida = (estado_final["ram_usada_gb"] - estado_inicial["ram_usada_gb"])
    print(f"\n  RESUMEN:")
    print(f"  Bloques agregados       : {bloques:,}")
    print(f"  Total strings en RAM    : {len(contenedor):,}")
    tam_gb = (len(contenedor) * TAMANO_STRING) / (1024 ** 3)
    print(f"  Datos asignados (~)     : {tam_gb:.3f} GB")
    print(f"  RAM consumida adicional : {memoria_consumida:.2f} GB")
    print(f"  Uso de SWAP al final    : {estado_final['swap_usada_gb']:.2f} GB"
          f"  ({estado_final['swap_pct']:.1f}%)")

    # Liberar la memoria explícitamente
    print(f"\n  Liberando memoria...")
    del contenedor
    time.sleep(1)
    estado_post = obtener_estado_memoria()
    print(f"  RAM tras liberar: {estado_post['ram_usada_gb']:.2f} GB"
          f"  ({estado_post['ram_pct']:.1f}%)")
    print("\n  Demostración completada.")


if __name__ == "__main__":
    main()
