import heapq

# Definir la posición objetivo para cada valor del puzzle
goal_state = {
    1: (0, 0), 2: (0, 1), 3: (0, 2),
    4: (1, 2), 5: (2, 2), 6: (2, 1),
    7: (2, 0), 8: (1, 0), 0: (1, 1)
}


# Función para calcular la distancia de Manhattan
def manhattan_distance(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            value = state[i][j]
            if value != 0:
                goal_pos = goal_state[value]
                distance += abs(i - goal_pos[0]) + abs(j - goal_pos[1])
    return distance


# Función para convertir el estado en una tupla inmutable
def tuple_state(state):
    return tuple(tuple(row) for row in state)


# Función para encontrar la posición del 0 (vacío)
def find_zero(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j


# Generar estados sucesores moviendo el espacio vacío
def generate_successors(state):
    zero_row, zero_col = find_zero(state)
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Movimientos: abajo, arriba, derecha, izquierda
    successors = []

    for dr, dc in directions:
        new_row, new_col = zero_row + dr, zero_col + dc
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            # Crear un nuevo estado intercambiando el 0
            new_state = [list(row) for row in state]
            new_state[zero_row][zero_col], new_state[new_row][new_col] = new_state[new_row][new_col], \
            new_state[zero_row][zero_col]
            successors.append(new_state)

    return successors


# Algoritmo A* para resolver el 8-puzzle
def a_star_solver(start_state):
    open_list = []  # Lista de prioridades (heapq)
    closed_set = set()  # Conjunto de nodos ya visitados
    came_from = {}  # Mantiene el camino hacia el nodo actual

    g_costs = {tuple_state(start_state): 0}  # Costo del camino hasta el nodo actual
    h_cost = manhattan_distance(start_state)  # Heurística (distancia de Manhattan)
    f_cost = h_cost  # f = g + h

    heapq.heappush(open_list, (f_cost, start_state))  # Añadir el nodo inicial

    while open_list:
        # Extraer el nodo con el menor costo f
        _, current_state = heapq.heappop(open_list)
        current_tuple = tuple_state(current_state)

        # Si hemos alcanzado el estado objetivo
        if current_state == [[1, 2, 3], [8, 0, 4], [7, 6, 5]]:
            return reconstruct_path(came_from, current_tuple)

        closed_set.add(current_tuple)  # Añadir a la lista cerrada

        # Generar sucesores
        for successor in generate_successors(current_state):
            successor_tuple = tuple_state(successor)
            if successor_tuple in closed_set:
                continue  # Si ya fue explorado, lo saltamos

            # Cálculo de costos
            tentative_g = g_costs[current_tuple] + 1  # Siempre hay un costo de 1 por movimiento

            if successor_tuple not in g_costs or tentative_g < g_costs[successor_tuple]:
                # Registrar el camino
                came_from[successor_tuple] = current_tuple
                g_costs[successor_tuple] = tentative_g
                h_cost = manhattan_distance(successor)
                f_cost = tentative_g + h_cost

                heapq.heappush(open_list, (f_cost, successor))  # Añadir a la lista abierta

    return None  # Si no se encuentra solución


# Función para reconstruir el camino desde el nodo objetivo hasta el nodo inicial
def reconstruct_path(came_from, current_tuple):
    total_path = [current_tuple]
    while current_tuple in came_from:
        current_tuple = came_from[current_tuple]
        total_path.append(current_tuple)
    total_path.reverse()
    return total_path


# Estado inicial (puedes modificarlo)
start_state = [
    [2, 8, 5],
    [3, 0, 6],
    [4, 7, 1]
]

# Resolver el puzzle
solution = a_star_solver(start_state)

if solution:
    print("Solución encontrada en", len(solution) - 1, "movimientos.")
    for step in solution:
        for row in step:
            print(row)
        print()
else:
    print("No se encontró solución.")
