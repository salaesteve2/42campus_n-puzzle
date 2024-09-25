from colorama import Fore, Style
from src import path, heuristics, solution
import heapq

# Función para convertir el estado en una tupla inmutable
def tuple_state(state):
    return tuple(tuple(row) for row in state)

def a_algorithm(mode, args, matriz, matrix_snale, size, start_time):
    visited = set()
    open_set = {}
    maps_list = []
    recorrido = {}
    g_cost = {0: 0}

    # Gestionar greedy search
    if not args.greedy_search:
        g_cost = {tuple_state(matriz): 0}
        print('Greedy Search:' + Fore.RED + ' False' + Style.RESET_ALL)
    else:
        print('Greedy Search:' + Fore.GREEN + ' True' + Style.RESET_ALL)

    # Gestionar heuristica
    h_cost = heuristics.heuristic(mode, matriz, matrix_snale, size, args)
    f_cost = h_cost

    heapq.heappush(maps_list, (f_cost, matriz))
    open_set[tuple_state(matriz)] = f_cost

    # Bucle principal
    while maps_list:
        _, estado_actual = heapq.heappop(maps_list)
        lista_actual = tuple_state(estado_actual)

        # Datos a imprimir si hay solución
        if estado_actual == matrix_snale:
            solution.solution(open_set, visited, start_time, recorrido, lista_actual, size, args)

        visited.add(lista_actual)

        # generar movimientos
        for sucesores in path.generar_sucesores(size, estado_actual):
            lista_sucesores = tuple_state(sucesores)

            # Matriz ya vista, se pasa a la siguiente
            if lista_sucesores in visited:
                continue

            # Gestionar greedy search
            posibilidad_g = heuristics.greedy_search(args, g_cost, lista_actual)

            # Gestión si el costo es menor que la tupla anterior
            if lista_sucesores not in g_cost or posibilidad_g < g_cost[lista_sucesores]:
                recorrido[lista_sucesores] = lista_actual
                g_cost[lista_sucesores] = posibilidad_g

                # Aplicar heuristica correspondiente
                h_cost, posibilidad_g = heuristics.next_heuristic(mode, size, sucesores, matrix_snale, posibilidad_g, args)

                # Greedy search
                if args.greedy_search:
                    posibilidad_g = 0

                # Costo total
                f_cost = posibilidad_g + h_cost

                # Meter tupla si el cambio se queda
                if lista_sucesores not in open_set or f_cost < open_set[lista_sucesores]:
                    open_set[lista_sucesores] = f_cost
                    heapq.heappush(maps_list, (f_cost, sucesores))