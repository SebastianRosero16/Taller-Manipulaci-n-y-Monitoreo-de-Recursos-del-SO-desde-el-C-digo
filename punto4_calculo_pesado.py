"""
Punto 4 - Script de Cálculo Pesado
====================================
Este script realiza un cálculo matemático intensivo (números primos).
Es ejecutado por punto4_prioridad_procesos.py con distintas prioridades.

Recibe un argumento por línea de comandos:
  - argv[1]: etiqueta de la instancia (ej: "BAJA" o "TIEMPO_REAL")

Al terminar imprime el tiempo total de ejecución.
"""

import sys
import time
import math

# Etiqueta de esta instancia (pasada como argumento)
etiqueta = sys.argv[1] if len(sys.argv) > 1 else "SIN_ETIQUETA"

LIMITE = 500_000   # calcular primos hasta este número


def es_primo(n: int) -> bool:
    """Comprueba si n es primo."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


inicio = time.time()

# Cálculo pesado: contar todos los primos hasta LIMITE
total_primos = sum(1 for n in range(2, LIMITE + 1) if es_primo(n))

fin    = time.time()
tiempo = fin - inicio

# Resultado que el lanzador leerá desde stdout
print(f"{etiqueta}|{tiempo:.4f}|{total_primos}")
