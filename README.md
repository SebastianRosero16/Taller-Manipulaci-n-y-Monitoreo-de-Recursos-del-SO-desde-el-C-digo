# Taller: Manipulación y Monitoreo de Recursos del SO desde el Código

Taller de la materia de **Sistemas Operativos** — VI Semestre.  
Todo está hecho en **Python** usando la librería `psutil`.

---

## ¿Cómo ejecutar los scripts?

Primero hay que tener instalada la librería psutil. Si no la tienes, la instalas así:

```bash
pip install psutil
```

---

## Punto 1 — Vigilante de Recursos

La idea de este punto era hacer un script que estuviera mirando en tiempo real cuánta RAM y CPU está usando el computador, como si fuera un pequeño panel de control.

Lo que hace es revisar cada 2 segundos los porcentajes de uso y mostrarlos en consola con una barra. Si la RAM supera el 80%, guarda una alerta en un archivo de texto llamado `alertas_ram.txt` con la hora exacta y los valores en ese momento.

Para correrlo:
```bash
py -3.11 punto1_vigilante_recursos.py
```

Para pararlo se presiona `Ctrl+C`.

**Archivos:**
- `punto1_vigilante_recursos.py`
- `alertas_ram.txt` (se genera solo cuando corre el script)

---

## Punto 2 — Simulador de Caché

Acá la idea era entender por qué el sistema operativo no va al disco cada vez que necesita un dato, sino que guarda las cosas en RAM para no repetir el trabajo.

El programa lee un archivo grande. La primera vez lo lee del disco y lo guarda en un diccionario (que hace las veces de caché). Las siguientes veces que lo "lee", en realidad lo saca del diccionario que está en RAM. Se mide el tiempo de ambos casos con `time.time()` y la diferencia es enorme.

Primero hay que generar el archivo de prueba:
```bash
py -3.11 generar_archivo_grande.py
```
Luego se corre el simulador:
```bash
py -3.11 punto2_simulador_cache.py
```

**Archivos:**
- `punto2_simulador_cache.py`
- `generar_archivo_grande.py`

---

## Punto 3 — Estrés de Memoria

Este punto era para ver en la práctica qué pasa cuando se le acaba la RAM física al computador. El script va llenando una lista con millones de strings hasta que la RAM se llena y el sistema operativo empieza a usar la memoria virtual (swap).

Se puede ver en el Administrador de Tareas cómo la memoria "comprometida" empieza a subir más allá de la RAM física disponible. Para no bloquear el computador tiene un límite de seguridad que para el script cuando la RAM llega al 85%.

```bash
py -3.11 punto3_estres_memoria.py
```

> Se recomienda abrir el Administrador de Tareas antes de correrlo (Ctrl+Shift+Esc → Rendimiento → Memoria) para ver el efecto en tiempo real.

**Archivos:**
- `punto3_estres_memoria.py`

---

## Punto 4 — Prioridad de Procesos

Acá aprendimos que no todos los procesos son iguales para el sistema operativo. Usando `psutil` se puede cambiar la prioridad de un proceso y eso afecta qué tan rápido lo atiende el Kernel.

El script lanza dos veces el mismo cálculo matemático (buscar números primos hasta 500,000) al mismo tiempo, pero uno con prioridad **Baja (IDLE)** y otro con prioridad **Tiempo Real (REALTIME)**. Al final compara cuál terminó primero.

Para que funcione el REALTIME hay que correrlo como Administrador (clic derecho en cmd → Ejecutar como administrador).

```bash
py -3.11 punto4_prioridad_procesos.py
```

**Archivos:**
- `punto4_prioridad_procesos.py`
- `punto4_calculo_pesado.py` (es el script del cálculo, lo llama el lanzador)
