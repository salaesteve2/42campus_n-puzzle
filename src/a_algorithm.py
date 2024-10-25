from colorama import Fore, Style
from src import path, heuristics, solution
import heapq

# Función para convertir el estado en una tupla inmutable
def tuple_state(state):
    return tuple(tuple(row) for row in state)

def a_algorithm(mode, args, matrix, matrix_snale, size, start_time):
    visited = set()
    open_set = {}
    maps_list = []
    route = {}
    g_cost = {0: 0}

    # Gestionar greedy search
    if not args.greedy_search:
        g_cost = {tuple_state(matrix): 0}
        print('Greedy Search:' + Fore.RED + ' False' + Style.RESET_ALL)
    else:
        print('Greedy Search:' + Fore.GREEN + ' True' + Style.RESET_ALL)

    # Gestionar heuristica
    h_cost = heuristics.heuristic(mode, matrix, matrix_snale, size, args)
    f_cost = h_cost

    heapq.heappush(maps_list, (f_cost, matrix))
    open_set[tuple_state(matrix)] = f_cost

    # Bucle principal
    while maps_list:
        _, actual_state = heapq.heappop(maps_list)
        actual_list = tuple_state(actual_state)

        # Datos a imprimir si hay solución
        if actual_state == matrix_snale:
            solution.solution(open_set, visited, start_time, route, actual_list, size, args)

        visited.add(actual_list)

        # generar movimientos
        for successors in path.generate_next(size, actual_state):
            successors_list = tuple_state(successors)

            # Matriz ya vista, se pasa a la siguiente
            if successors_list in visited:
                continue

            # Gestionar greedy search
            posibility_g = heuristics.greedy_search(args, g_cost, actual_list)

            # Gestión si el costo es menor que la tupla anterior
            if successors_list not in g_cost or posibility_g < g_cost[successors_list]:
                route[successors_list] = actual_list
                g_cost[successors_list] = posibility_g

                # Aplicar heuristica correspondiente
                h_cost, posibility_g = heuristics.next_heuristic(mode, size, successors, matrix_snale, posibility_g, args)

                # Greedy search
                if args.greedy_search:
                    posibility_g = 0

                # Costo total
                f_cost = posibility_g + h_cost

                # Meter tupla si el cambio se queda
                if successors_list not in open_set or f_cost < open_set[successors_list]:
                    open_set[successors_list] = f_cost
                    heapq.heappush(maps_list, (f_cost, successors))