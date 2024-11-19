import random
from collections import deque

class Proceso:
    def __init__(self, nombre, llegada, duracion):
        self.nombre = nombre
        self.llegada = llegada
        self.duracion = duracion
        self.tiempo_restante = duracion

def generar_procesos(n):
    procesos = []
    tiempo_llegada = 0
    for i in range(n):
        duracion = random.randint(2, 7) 
        procesos.append(Proceso(chr(65 + i), tiempo_llegada, duracion))
        tiempo_llegada += random.randint(1, 4)
    return procesos

def fcfs(procesos):
    tiempo = 0
    tiempos_finalizacion = []
    for proceso in procesos:
        if tiempo < proceso.llegada:
            tiempo = proceso.llegada
        tiempo += proceso.duracion
        tiempos_finalizacion.append(tiempo)
    return tiempos_finalizacion

def rr(procesos, quantum):
    tiempo = 0
    cola = deque([p for p in procesos if p.llegada <= tiempo])
    procesos_pendientes = deque([p for p in procesos if p.llegada > tiempo])
    tiempos_finalizacion = {}

    while cola or procesos_pendientes:
        if not cola and procesos_pendientes:
            tiempo = procesos_pendientes[0].llegada
            cola.append(procesos_pendientes.popleft())

        proceso = cola.popleft()
        tiempo_proceso = min(proceso.tiempo_restante, quantum)
        proceso.tiempo_restante -= tiempo_proceso
        tiempo += tiempo_proceso

        if proceso.tiempo_restante == 0:
            tiempos_finalizacion[proceso.nombre] = tiempo
        else:
            cola.append(proceso)

        while procesos_pendientes and procesos_pendientes[0].llegada <= tiempo:
            cola.append(procesos_pendientes.popleft())

    return [tiempos_finalizacion[p.nombre] for p in procesos]

def spn(procesos):
    tiempo = 0
    tiempos_finalizacion = []
    lista_espera = sorted(procesos, key=lambda p: (p.llegada, p.duracion))
    while lista_espera:
        candidatos = [p for p in lista_espera if p.llegada <= tiempo]
        if not candidatos:
            tiempo = lista_espera[0].llegada
            candidatos = [lista_espera[0]]

        proceso = min(candidatos, key=lambda p: p.duracion)
        lista_espera.remove(proceso)
        tiempo += proceso.duracion
        tiempos_finalizacion.append(tiempo)

    return tiempos_finalizacion

def calcular_metricas(tiempos_finalizacion, procesos):
    n = len(procesos)
    tiempo_total = sum(tiempos_finalizacion) / n
    tiempo_espera = sum([t - p.llegada - p.duracion for t, p in zip(tiempos_finalizacion, procesos)]) / n
    penalizacion = sum([t / p.duracion for t, p in zip(tiempos_finalizacion, procesos)]) / n
    return tiempo_total, tiempo_espera, penalizacion

def ejecutar_simulacion():
    procesos = generar_procesos(5)
    print("Procesos:")
    for p in procesos:
        print(f"{p.nombre}: llegada={p.llegada}, duración={p.duracion}")
    print(" ")

    print("- FCFS:")
    fcfs_resultados = fcfs(procesos)
    fcfs_metricas = calcular_metricas(fcfs_resultados, procesos)
    print(f"FCFS: T={fcfs_metricas[0]:.2f}, E={fcfs_metricas[1]:.2f}, P={fcfs_metricas[2]:.2f}")

    print("- RR1 (Quantum=1):")
    rr1_resultados = rr(procesos, quantum=1)
    rr1_metricas = calcular_metricas(rr1_resultados, procesos)
    print(f"RR1: T={rr1_metricas[0]:.2f}, E={rr1_metricas[1]:.2f}, P={rr1_metricas[2]:.2f}")

    print("- RR4 (Quantum=4):")
    rr4_resultados = rr(procesos, quantum=4)
    rr4_metricas = calcular_metricas(rr4_resultados, procesos)
    print(f"RR4: T={rr4_metricas[0]:.2f}, E={rr4_metricas[1]:.2f}, P={rr4_metricas[2]:.2f}")

    print("- SPN:")
    spn_resultados = spn(procesos)
    spn_metricas = calcular_metricas(spn_resultados, procesos)
    print(f"SPN: T={spn_metricas[0]:.2f}, E={spn_metricas[1]:.2f}, P={spn_metricas[2]:.2f}")

#Ejecutar 5 veces
for i in range(5):
    print(f"\nRonda {i + 1}")
    ejecutar_simulacion()

