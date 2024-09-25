import argparse
import sys
import os
import heapq
import time
from colorama import Fore, Style, init
from src import maps, path, is_solvable, heuristics, visualizer


# Función para convertir el estado en una tupla inmutable
def tuple_state(state):
    return tuple(tuple(row) for row in state)

def main():
    init()
    start_time = time.time()

    # Gestion argumentos
    parser = argparse.ArgumentParser()
    parser.add_argument("map", help="Map puzzle's side.")
    parser.add_argument("mode", help="Heuristic function(Manhattan, Hamming, Costo Uniforme, Nilsson).")
    parser.add_argument("-g", "--greedy_search", action="store_true", default=False, help="Greedy Search function.")
    parser.add_argument("-v", "--visualizer", action="store_true", default=False ,help="Visualizer.")
    args = parser.parse_args()


    # Parsear los argumentos
    if not os.path.exists(args.map):
        print(Fore.RED + "Error. The map dont exist." + Style.RESET_ALL)
        sys.exit()

    modes = {
        "Manhattan": "Manhattan",
        "Hamming": "Hamming",
        "Costo Uniforme": "Costo Uniforme",
        "Nilsson": "Nilsson"
    }

    mode = args.mode
    if mode not in modes:
        print(Fore.RED + "Error. The mode dont exist." + Style.RESET_ALL)
        sys.exit()

    # Abrir archivo
    lines = maps.leer_mapa(args.map)

    # Parsear mapa
    matriz, size = maps.procesar_mapa(lines)
    matrix = [number for sublist in matriz for number in sublist]
    rango = all(0 <= num <= size * size - 1 for num in matrix)

    # gestion de posibles errores
    if len(matrix) != (size * size) or len(matrix) != len(set(matrix)) or not rango:
        print(Fore.RED + 'Error. The map is not correct.' + Style.RESET_ALL)
        sys.exit(1)

    #Matriz del mapa ordenado
    matrix_snale = maps.generar_matriz_caracol(size)
    print("Desired matrix: ")
    for lines in matrix_snale:
        print(Fore.YELLOW + str(lines) + Style.RESET_ALL)

    #Matriz del mapa a ordenar
    print("Initial matrix: ")
    for lines in matriz:
        print(Fore.CYAN + str(lines) + Style.RESET_ALL)

    # Calcular si es resoluble
    matrix_snale_aplanado = [number for sublist in matrix_snale for number in sublist]
    if not is_solvable.is_solvable(matrix, matrix_snale_aplanado, size):
        print('Solvable:' + Fore.RED + ' False' + Style.RESET_ALL)
        sys.exit(1)
    else:
        print('Solvable:'+ Fore.GREEN + ' True' + Style.RESET_ALL)

    if args.visualizer:
        print('Visualizer: ' + Fore.GREEN + 'True' + Style.RESET_ALL)
    else:
        print('Visualizer:' + Fore.RED + ' False' + Style.RESET_ALL)

    # Aplicar algoritmo solucion
    visited = set()
    open_set = {}
    maps_list = []
    recorrido = {}
    g_cost = {0: 0}
    h_cost = 0

    # Gestionar greedy search
    if not args.greedy_search:
        g_cost = {tuple_state(matriz): 0}
        print('Greedy Search:' + Fore.RED +' False' + Style.RESET_ALL)
    else:
        print('Greedy Search:' + Fore.GREEN + ' True' + Style.RESET_ALL)

    # Gestionar heuristica
    if mode == "Manhattan":
        print('Heuristic: ' + Fore.LIGHTMAGENTA_EX + 'Manhattan' + Style.RESET_ALL)
        h_cost = heuristics.distance_manhattan(size, matriz, matrix_snale)
    elif mode == "Hamming":
        print('Heuristic: ' + Fore.LIGHTMAGENTA_EX + 'Hamming' + Style.RESET_ALL)
        h_cost = heuristics.hamming(matriz, matrix_snale)
    elif mode == "Costo Uniforme":
        print('Heuristic: ' + Fore.LIGHTMAGENTA_EX + 'Costo Uniforme' + Style.RESET_ALL)
        h_cost = 0
    elif mode == "Nilsson":
        print('Heuristic: ' + Fore.LIGHTMAGENTA_EX + 'Nilsson' + Style.RESET_ALL)
        h_cost = heuristics.distance_manhattan(size, matriz, matrix_snale)
    f_cost = h_cost

    heapq.heappush(maps_list, (f_cost, matriz))
    open_set[tuple_state(matriz)] = f_cost


    spiral_sequence = heuristics.generate_spiral_sequence(size)

    # Bucle principal
    while maps_list:
        _, estado_actual = heapq.heappop(maps_list)
        lista_actual = tuple_state(estado_actual)

        # Datos a imprimir si hay solución
        if estado_actual == matrix_snale:

            print(Fore.GREEN +"Solution found" + Style.RESET_ALL)
            print('Total number of states selected (time complexity): ' + Fore.GREEN + str(len(open_set)) + Style.RESET_ALL) # cantidad de nodos a lo largo de la ejecucion
            print('Total number of states in memory (space complexity): ' + Fore.GREEN + str(len(visited)) + Style.RESET_ALL) # #cantidad de nodos que fueron visitados y alamacenados en el momento de encontrar la solucion
            end_time = time.time()
            execution_time = end_time - start_time
            print('Execution time: ' + Fore.GREEN +f"{execution_time:.5f}" + ' seconds' + Style.RESET_ALL)
            camino = path.camino_recorrido(recorrido, lista_actual)

            # Llamar al visualizador
            if args.visualizer:
                visualizer.visualizador_solucion(camino, size)

            sys.exit(0)
        visited.add(lista_actual)

        # generar movimientos
        for sucesores in path.generar_sucesores(size, estado_actual):
            lista_sucesores = tuple_state(sucesores)

            # Matriz ya vista, se pasa a la siguiente
            if lista_sucesores in visited:
                continue

            # Gestionar greedy search
            if not args.greedy_search:
                posibilidad_g = g_cost[lista_actual] + 1
            else:
                posibilidad_g = 0

            # Gestión si el costo es menor que la tupla anterior
            if lista_sucesores not in g_cost or posibilidad_g < g_cost[lista_sucesores]:
                recorrido[lista_sucesores] = lista_actual
                g_cost[lista_sucesores] = posibilidad_g

                # Aplicar heuristica correspondiente
                if mode == "Manhattan":
                    h_cost = heuristics.distance_manhattan(size, sucesores, matrix_snale)
                elif mode == "Hamming":
                    h_cost = heuristics.hamming(sucesores, matrix_snale)
                elif mode == "Costo Uniforme":
                    h_cost = 0
                elif mode == "Nilsson":
                    posibilidad_g = heuristics.nilsson(sucesores, spiral_sequence, size) * 3
                    h_cost = heuristics.distance_manhattan(size, sucesores, matrix_snale)

                # Greedy search
                if args.greedy_search:
                    posibilidad_g = 0

                # Costo total
                f_cost = posibilidad_g + h_cost

                # Meter tupla si el cambio se queda
                if lista_sucesores not in open_set or f_cost < open_set[lista_sucesores]:
                    open_set[lista_sucesores] = f_cost
                    heapq.heappush(maps_list, (f_cost, sucesores))

if __name__ == "__main__":
    main()
