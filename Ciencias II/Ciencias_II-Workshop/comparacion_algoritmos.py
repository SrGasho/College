
"""
Archivo: /mnt/data/comparacion_caminos_cortos.py

Laboratorio de comparación de eficiencia para:
- Dijkstra
- Bellman-Ford
- Floyd-Warshall

Vamos a:
1. Generar grafos aleatorios dirigidos.
2. Ejecutar los algoritmos sobre los mismos grafos.
3. Medir tiempos de ejecución promedio.
4. Comparar resultados entre algoritmos.
5. Incluimos un escenario con pesos positivos y otro con pesos negativos
   (sin ciclos negativos garantizados por construcción).

Nota :3
- Para grafos con pesos negativos, NO se ejecuta Dijkstra.
"""

from __future__ import annotations

import math
import random
import time
import heapq
from statistics import mean
from typing import Dict, List, Tuple, Optional

# Tipos


Nodo = int
Peso = float
Arista = Tuple[Nodo, Nodo, Peso]
GrafoLista = Dict[Nodo, List[Tuple[Nodo, Peso]]]



# Algoritmos


def dijkstra(grafo: GrafoLista, inicio: Nodo) -> Dict[Nodo, Peso]:
    """Usando Dijkstra.

    Requiere que todos los pesos no sean negativos.
    """
    distancias = {nodo: math.inf for nodo in grafo}
    distancias[inicio] = 0.0

    cola: List[Tuple[Peso, Nodo]] = [(0.0, inicio)]

    while cola:
        distancia_actual, nodo_actual = heapq.heappop(cola)

        if distancia_actual > distancias[nodo_actual]:
            continue

        for vecino, peso in grafo[nodo_actual]:
            nueva_distancia = distancia_actual + peso
            if nueva_distancia < distancias[vecino]:
                distancias[vecino] = nueva_distancia
                heapq.heappush(cola, (nueva_distancia, vecino))

    return distancias


def bellman_ford(vertices: List[Nodo], aristas: List[Arista], inicio: Nodo) -> Dict[Nodo, Peso]:
    """usando Bellman-Ford.

    Soporta pesos negativos y detecta ciclos negativos.
    """
    distancias = {v: math.inf for v in vertices}
    distancias[inicio] = 0.0

    n = len(vertices)

    for _ in range(n - 1):
        hubo_cambio = False
        for u, v, peso in aristas:
            if distancias[u] != math.inf and distancias[u] + peso < distancias[v]:
                distancias[v] = distancias[u] + peso
                hubo_cambio = True
        if not hubo_cambio:
            break

    for u, v, peso in aristas:
        if distancias[u] != math.inf and distancias[u] + peso < distancias[v]:
            raise ValueError("El grafo contiene un ciclo negativo.")

    return distancias


def floyd_warshall(matriz: List[List[Peso]]) -> List[List[Peso]]:
    """Calcula todas las distancias mínimas entre todos los pares de nodos."""
    n = len(matriz)
    dist = [fila[:] for fila in matriz]

    for k in range(n):
        for i in range(n):
            dik = dist[i][k]
            if dik == math.inf:
                continue
            for j in range(n):
                nueva = dik + dist[k][j]
                if nueva < dist[i][j]:
                    dist[i][j] = nueva

    return dist


# Generación y conversión de grafos


def generar_grafo_dirigido(
    num_nodos: int,
    densidad: float,
    rango_pesos: Tuple[int, int],
    permitir_negativos: bool = False,
    semilla: Optional[int] = None,
) -> Tuple[GrafoLista, List[Nodo], List[Arista]]:
    """Genera un grafo dirigido aleatorio.
    """
    if semilla is not None:
        random.seed(semilla)

    vertices = list(range(num_nodos))
    grafo: GrafoLista = {i: [] for i in vertices}
    aristas: List[Arista] = []

    min_peso, max_peso = rango_pesos

    if permitir_negativos:
        # DAG: solo aristas hacia adelante para evitar ciclos negativos.
        for u in range(num_nodos):
            for v in range(u + 1, num_nodos):
                if random.random() < densidad:
                    peso = random.randint(min_peso, max_peso)
                    grafo[u].append((v, float(peso)))
                    aristas.append((u, v, float(peso)))
    else:
        for u in range(num_nodos):
            for v in range(num_nodos):
                if u != v and random.random() < densidad:
                    peso = random.randint(min_peso, max_peso)
                    grafo[u].append((v, float(peso)))
                    aristas.append((u, v, float(peso)))

    return grafo, vertices, aristas


def lista_a_matriz(num_nodos: int, aristas: List[Arista]) -> List[List[Peso]]:
    """Convierte lista de aristas a matriz de adyacencia (ponderada)"""
    matriz = [[math.inf] * num_nodos for _ in range(num_nodos)]
    for i in range(num_nodos):
        matriz[i][i] = 0.0

    for u, v, peso in aristas:
        if peso < matriz[u][v]:
            matriz[u][v] = peso

    return matriz



# Validación


def comparar_resultados_fuente_unica(
    d1: Dict[Nodo, Peso],
    d2: Dict[Nodo, Peso],
    tolerancia: float = 1e-9
) -> bool:
    """Compara dos diccionarios de distancias."""
    if d1.keys() != d2.keys():
        return False

    for k in d1:
        a = d1[k]
        b = d2[k]
        if math.isinf(a) and math.isinf(b):
            continue
        if abs(a - b) > tolerancia:
            return False
    return True


def distancias_desde_matriz(distancias_todos_pares: List[List[Peso]], origen: Nodo) -> Dict[Nodo, Peso]:
    """Extrae desde la matriz de Floyd-Warshall las distancias de un origen."""
    return {j: distancias_todos_pares[origen][j] for j in range(len(distancias_todos_pares))}



# Medición de tiempos


def medir_tiempo(func, *args, repeticiones: int = 3, **kwargs) -> Tuple[float, object]:
    """Mide el tiempo promedio de ejecución de una función."""
    tiempos = []
    resultado = None

    for _ in range(repeticiones):
        inicio = time.perf_counter()
        resultado = func(*args, **kwargs)
        fin = time.perf_counter()
        tiempos.append(fin - inicio)

    return mean(tiempos), resultado



# Experimentos


def experimento_pesos_positivos() -> None:
    print("EXPERIMENTO 1: GRAFOS CON PESOS POSITIVOS")
    print("En este escenario se comparan Dijkstra, Bellman-Ford y Floyd-Warshall.")
    print()

    # Floyd-Warshall crece muy rápido, así que aquí usamos tamaños manejables.
    escenarios = [
        {"nodos": 10, "densidad": 0.30, "repeticiones": 5},
        {"nodos": 30, "densidad": 0.20, "repeticiones": 3},
        {"nodos": 60, "densidad": 0.15, "repeticiones": 2},
    ]

    encabezado = f"{'Nodos':>8} | {'Aristas':>8} | {'Dijkstra (s)':>14} | {'Bellman-Ford (s)':>18} | {'Floyd-Warshall (s)':>18} | {'Resultados iguales':>18}"
    print(encabezado)
    print("-" * len(encabezado))

    for i, config in enumerate(escenarios, start=1):
        n = config["nodos"]
        densidad = config["densidad"]
        repeticiones = config["repeticiones"]

        grafo, vertices, aristas = generar_grafo_dirigido(
            num_nodos=n,
            densidad=densidad,
            rango_pesos=(1, 20),
            permitir_negativos=False,
            semilla=100 + i,
        )
        matriz = lista_a_matriz(n, aristas)

        origen = 0

        tiempo_dijkstra, resultado_dijkstra = medir_tiempo(
            dijkstra, grafo, origen, repeticiones=repeticiones
        )
        tiempo_bellman, resultado_bellman = medir_tiempo(
            bellman_ford, vertices, aristas, origen, repeticiones=repeticiones
        )
        tiempo_floyd, resultado_floyd = medir_tiempo(
            floyd_warshall, matriz, repeticiones=repeticiones
        )

        distancias_floyd = distancias_desde_matriz(resultado_floyd, origen)

        iguales = (
            comparar_resultados_fuente_unica(resultado_dijkstra, resultado_bellman)
            and comparar_resultados_fuente_unica(resultado_dijkstra, distancias_floyd)
        )

        print(
            f"{n:>8} | {len(aristas):>8} | {tiempo_dijkstra:>14.6f} | "
            f"{tiempo_bellman:>18.6f} | {tiempo_floyd:>18.6f} | {str(iguales):>18}"
        )



def experimento_pesos_negativos() -> None:
    
    print("EXPERIMENTO 2: GRAFOS CON PESOS NEGATIVOS (SIN CICLOS NEGATIVOS)")
    print("En este escenario se comparan Bellman-Ford y Floyd-Warshall.")
    print("Dijkstra no se ejecuta porque no garantiza resultados correctos con pesos negativos.")
    print()

    escenarios = [
        {"nodos": 10, "densidad": 0.35, "repeticiones": 5},
        {"nodos": 25, "densidad": 0.20, "repeticiones": 3},
        {"nodos": 50, "densidad": 0.12, "repeticiones": 2},
    ]

    encabezado = f"{'Nodos':>8} | {'Aristas':>8} | {'Bellman-Ford (s)':>18} | {'Floyd-Warshall (s)':>18} | {'Resultados iguales':>18}"
    print(encabezado)
    print("-" * len(encabezado))

    for i, config in enumerate(escenarios, start=1):
        n = config["nodos"]
        densidad = config["densidad"]
        repeticiones = config["repeticiones"]

        grafo, vertices, aristas = generar_grafo_dirigido(
            num_nodos=n,
            densidad=densidad,
            rango_pesos=(-5, 15),
            permitir_negativos=True,
            semilla=200 + i,
        )
        matriz = lista_a_matriz(n, aristas)

        origen = 0

        tiempo_bellman, resultado_bellman = medir_tiempo(
            bellman_ford, vertices, aristas, origen, repeticiones=repeticiones
        )
        tiempo_floyd, resultado_floyd = medir_tiempo(
            floyd_warshall, matriz, repeticiones=repeticiones
        )

        distancias_floyd = distancias_desde_matriz(resultado_floyd, origen)
        iguales = comparar_resultados_fuente_unica(resultado_bellman, distancias_floyd)

        print(
            f"{n:>8} | {len(aristas):>8} | "
            f"{tiempo_bellman:>18.6f} | {tiempo_floyd:>18.6f} | {str(iguales):>18}"
        )


def ejemplo_basico() -> None:
    print("EJEMPLO DEL LABORATORIO")

    grafo = {
        0: [(1, 4.0), (2, 2.0)],
        1: [(2, 5.0), (3, 10.0)],
        2: [(4, 3.0)],
        3: [(5, 11.0)],
        4: [(3, 4.0)],
        5: [],
    }

    vertices = [0, 1, 2, 3, 4, 5]
    aristas = [
        (0, 1, 4.0),
        (0, 2, 2.0),
        (1, 2, 5.0),
        (1, 3, 10.0),
        (2, 4, 3.0),
        (4, 3, 4.0),
        (3, 5, 11.0),
    ]

    matriz = lista_a_matriz(len(vertices), aristas)

    print("Distancias con Dijkstra desde el nodo 0:")
    print(dijkstra(grafo, 0))
    print()

    print("Distancias con Bellman-Ford desde el nodo 0:")
    print(bellman_ford(vertices, aristas, 0))
    print()

    print("Matriz de distancias con Floyd-Warshall:")
    resultado = floyd_warshall(matriz)
    for fila in resultado:
        print(fila)
    print()


def main() -> None:
    ejemplo_basico()
    experimento_pesos_positivos()
    experimento_pesos_negativos()



if __name__ == "__main__":
    main()
