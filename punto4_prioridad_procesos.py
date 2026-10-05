"""
Punto 4 - Prioridad de Procesos (Scheduling)
=============================================
Concepto: Planificación de procesos del Kernel.

Lanza DOS instancias del mismo cálculo pesado en paralelo:
  - Instancia A → prioridad BAJA        (IDLE en Windows)
  - Instancia B → prioridad TIEMPO REAL (REALTIME en Windows)

Nota: REALTIME_PRIORITY_CLASS requiere ejecutar la terminal
como Administrador. Si no hay permisos suficientes, el script
cae automáticamente a HIGH_PRIORITY_CLASS e informa el cambio.

Para ejecutar como Administrador:
  1. Busca "cmd" en el menú Inicio
  2. Clic derecho → "Ejecutar como administrador"
  3. Navega a la carpeta del taller y corre:
       py -3.11 punto4_prioridad_procesos.py

Prioridades de Windows disponibles en psutil:
  psutil.IDLE_PRIORITY_CLASS          → Muy baja  (idle)
  psutil.BELOW_NORMAL_PRIORITY_CLASS  → Baja
  psutil.NORMAL_PRIORITY_CLASS        → Normal (por defecto)
  psutil.ABOVE_NORMAL_PRIORITY_CLASS  → Sobre lo normal
  psutil.HIGH_PRIORITY_CLASS          → Alta
  psutil.REALTIME_PRIORITY_CLASS      → Tiempo Real (requiere admin)
"""

import subprocess
import psutil
import sys
import time
import os

# ── Configuración ──────────────────────────────────────────────
PYTHON = sys.executable          # ruta al intérprete actual
SCRIPT = "punto4_calculo_pesado.py"

# Par de prioridades a comparar (Baja vs Tiempo Real)
INSTANCIAS = [
    {
        "etiqueta"   : "PRIORIDAD_BAJA",
        "prioridad"  : psutil.IDLE_PRIORITY_CLASS,
        "descripcion": "Idle / Baja",
        "fallback"   : None,   # sin fallback, siempre funciona
    },
    {
        "etiqueta"   : "TIEMPO_REAL",
        "prioridad"  : psutil.REALTIME_PRIORITY_CLASS,
        "descripcion": "Tiempo Real (REALTIME)",
        "fallback"   : psutil.HIGH_PRIORITY_CLASS,   # si no hay permisos de admin
    },
]
# ──────────────────────────────────────────────────────────────


def lanzar_con_prioridad(etiqueta: str, prioridad: int,
                          descripcion: str, fallback) -> subprocess.Popen:
    """
    Lanza punto4_calculo_pesado.py como subproceso y
    ajusta su prioridad con psutil inmediatamente.
    Si se deniega el acceso y hay un fallback, lo aplica.
    """
    proceso = subprocess.Popen(
        [PYTHON, SCRIPT, etiqueta],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    p = psutil.Process(proceso.pid)

    # Intentar aplicar la prioridad solicitada
    try:
        p.nice(prioridad)
        prioridad_aplicada = descripcion

    except psutil.AccessDenied:
        # Sin permisos de Administrador para REALTIME → usar fallback
        if fallback is not None:
            try:
                p.nice(fallback)
                prioridad_aplicada = (
                    f"High (fallback: REALTIME requiere admin)"
                )
            except psutil.AccessDenied:
                prioridad_aplicada = "Normal (sin permisos suficientes)"
        else:
            prioridad_aplicada = "Normal (sin permisos suficientes)"

    print(f"  PID {proceso.pid:6d}  |  {etiqueta:<20}  |  {prioridad_aplicada}")
    return proceso


def main() -> None:
    print("╔═══════════════════════════════════════════════════════╗")
    print("║   Punto 4 - Prioridad de Procesos (Scheduling)        ║")
    print("║   Baja (IDLE)  vs  Tiempo Real (REALTIME)             ║")
    print("╚═══════════════════════════════════════════════════════╝")
    print(f"\n  Script de cálculo : {SCRIPT}")
    print(f"  Intérprete Python  : {os.path.basename(PYTHON)}")
    print(f"\n  💡 Para activar REALTIME ejecuta como Administrador.")
    print(f"     Sin admin, la instancia TIEMPO_REAL usará HIGH.\n")

    if not os.path.exists(SCRIPT):
        print(f"  ⚠  No se encontró '{SCRIPT}' en el directorio actual.")
        print(f"     Asegúrate de ejecutar este script desde la misma carpeta.")
        return

    print("  Lanzando instancias en paralelo...")
    print(f"  {'─'*53}")

    inicio_global = time.time()
    procesos = []

    # Lanzar TODAS las instancias casi simultáneamente
    for cfg in INSTANCIAS:
        proc = lanzar_con_prioridad(**cfg)
        procesos.append({"config": cfg, "proceso": proc, "inicio": time.time()})

    print(f"  {'─'*53}")
    print(f"\n  Esperando resultados... (esto puede tardar ~30-60 seg)\n")

    resultados = []

    # Esperar a que cada proceso termine y recoger su salida
    for item in procesos:
        stdout, stderr = item["proceso"].communicate()   # bloquea hasta que termina
        tiempo_total   = time.time() - item["inicio"]

        # El script hijo imprime: etiqueta|tiempo|total_primos
        linea = stdout.strip()
        if "|" in linea:
            partes        = linea.split("|")
            etiqueta      = partes[0]
            tiempo_hijo   = float(partes[1])
            total_primos  = int(partes[2])
        else:
            etiqueta     = item["config"]["etiqueta"]
            tiempo_hijo  = tiempo_total
            total_primos = 0

        resultados.append({
            "etiqueta"    : etiqueta,
            "descripcion" : item["config"]["descripcion"],
            "tiempo"      : tiempo_hijo,
            "primos"      : total_primos,
            "pid"         : item["proceso"].pid,
        })

    # ── Resultados individuales ────────────────────────────────
    print(f"\n{'='*57}")
    print(f"  RESULTADOS")
    print(f"{'='*57}")
    for r in resultados:
        print(f"\n  {r['etiqueta']}")
        print(f"    Descripción  : {r['descripcion']}")
        print(f"    PID          : {r['pid']}")
        print(f"    Primos hallados: {r['primos']:,}")
        print(f"    Tiempo       : {r['tiempo']:.4f} segundos")

    # ── Comparativa final ──────────────────────────────────────
    if len(resultados) == 2:
        r_baja        = resultados[0]   # PRIORIDAD_BAJA  (IDLE)
        r_tiempo_real = resultados[1]   # TIEMPO_REAL     (REALTIME o HIGH)

        print(f"\n{'='*57}")
        print(f"  COMPARATIVA: Baja  vs  Tiempo Real")
        print(f"{'='*57}")
        print(f"  {r_baja['etiqueta']:<25}: {r_baja['tiempo']:.4f} s")
        print(f"  {r_tiempo_real['etiqueta']:<25}: {r_tiempo_real['tiempo']:.4f} s")

        diferencia = abs(r_baja['tiempo'] - r_tiempo_real['tiempo'])
        ganador    = (r_tiempo_real
                      if r_tiempo_real['tiempo'] < r_baja['tiempo']
                      else r_baja)

        print(f"\n  Ganador      : {ganador['etiqueta']}  ({ganador['tiempo']:.4f} s)")
        print(f"  Diferencia   : {diferencia:.4f} s  ({diferencia*1000:.1f} ms)")

        if diferencia > 0.05:
            ratio = max(r_baja['tiempo'], r_tiempo_real['tiempo']) / \
                    min(r_baja['tiempo'], r_tiempo_real['tiempo'])
            print(f"  La instancia TIEMPO_REAL fue {ratio:.2f}x más veloz que la BAJA.")
        else:
            print(f"  Diferencia muy pequeña: los CPUs modernos con múltiples")
            print(f"  núcleos pueden asignar núcleos distintos a cada proceso,")
            print(f"  reduciendo el impacto visible de la prioridad.")

        print(f"\n  → Conclusión: el Kernel asigna mayor quantum de CPU a procesos")
        print(f"    de alta prioridad (Tiempo Real). Eso significa que el scheduler")
        print(f"    los atiende antes en la cola de planificación, reduciendo")
        print(f"    el tiempo total de ejecución frente a un proceso de prioridad Baja.")

    print(f"\n  Tiempo total del experimento: {time.time() - inicio_global:.2f} s")
    print(f"{'='*57}\n")


if __name__ == "__main__":
    main()
