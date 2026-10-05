"""
Punto 1 - Vigilante de Recursos
================================
Concepto: Gestor de memoria y E/S del Sistema Operativo.

Monitorea en tiempo real el uso de RAM y CPU.
Genera una alerta en consola y guarda un log en 'alertas_ram.txt'
cada vez que la RAM supere el 80%.
"""

import psutil
import time
import datetime

# ── Configuración ──────────────────────────────────────────────
UMBRAL_RAM = 80          # porcentaje a partir del cual se genera alerta
INTERVALO  = 2           # segundos entre cada lectura
LOG_FILE   = "alertas_ram.txt"
# ───────────────────────────────────────────────────────────────


def guardar_log(mensaje: str) -> None:
    """Escribe una línea con timestamp en el archivo de log."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linea = f"[{timestamp}] {mensaje}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as archivo:
        archivo.write(linea)
    print(f"  ⚠  ALERTA guardada en '{LOG_FILE}'")


def obtener_metricas() -> dict:
    """Retorna un diccionario con el uso actual de CPU y RAM."""
    cpu_pct = psutil.cpu_percent(interval=1)          # % de uso de CPU
    ram     = psutil.virtual_memory()                  # objeto con datos de RAM
    return {
        "cpu_pct"  : cpu_pct,
        "ram_pct"  : ram.percent,         # porcentaje usado
        "ram_usada": ram.used  / (1024 ** 3),   # GB usados
        "ram_total": ram.total / (1024 ** 3),   # GB totales
    }


def mostrar_panel(metricas: dict) -> None:
    """Imprime el panel de control en la consola."""
    ahora = datetime.datetime.now().strftime("%H:%M:%S")
    ram_barra  = generar_barra(metricas["ram_pct"])
    cpu_barra  = generar_barra(metricas["cpu_pct"])

    print(f"\n{'='*50}")
    print(f"  Panel de Control del SO  |  {ahora}")
    print(f"{'='*50}")
    print(f"  CPU  : {cpu_barra} {metricas['cpu_pct']:5.1f}%")
    print(f"  RAM  : {ram_barra} {metricas['ram_pct']:5.1f}%"
          f"  ({metricas['ram_usada']:.2f} GB / {metricas['ram_total']:.2f} GB)")
    print(f"{'='*50}")


def generar_barra(porcentaje: float, largo: int = 20) -> str:
    """Genera una barra de progreso ASCII."""
    llenas = int(porcentaje / 100 * largo)
    return "[" + "█" * llenas + "░" * (largo - llenas) + "]"


def main() -> None:
    print("Iniciando Vigilante de Recursos...")
    print(f"Umbral de alerta RAM: {UMBRAL_RAM}%")
    print(f"Intervalo de lectura: {INTERVALO}s")
    print("Presiona Ctrl+C para detener.\n")

    try:
        while True:
            metricas = obtener_metricas()
            mostrar_panel(metricas)

            # ── Reto: guardar log si RAM supera el umbral ──
            if metricas["ram_pct"] > UMBRAL_RAM:
                mensaje = (
                    f"ALERTA - RAM al {metricas['ram_pct']:.1f}% "
                    f"({metricas['ram_usada']:.2f} GB usados de "
                    f"{metricas['ram_total']:.2f} GB) | "
                    f"CPU: {metricas['cpu_pct']:.1f}%"
                )
                print(f"\n  *** RAM supera el {UMBRAL_RAM}%: {metricas['ram_pct']:.1f}% ***")
                guardar_log(mensaje)

            time.sleep(INTERVALO)

    except KeyboardInterrupt:
        print("\n\nMonitoreo detenido por el usuario.")
        print(f"Revisa '{LOG_FILE}' para ver las alertas registradas.")


if __name__ == "__main__":
    main()
