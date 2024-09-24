def distance_manhattan(size1, matrix1, solved):
    res = 0
    for i, row in enumerate(matrix1):
        for j, value in enumerate(row):
            if value != 0 and value != solved[i][j]:
                target_x = (value - 1) // size1  # Calcula solo una vez el índice de fila objetivo
                target_y = (value - 1) % size1   # Calcula solo una vez el índice de columna objetivo
                res += abs(i - target_x) + abs(j - target_y)
    return res

def hamming(state, goal_state):
    count = 0
    for i in range(len(state)):
        if state[i] != goal_state[i] and state[i] != 0:  # Ignora el espacio vacío
            count += 1
    return count


def generate_spiral_sequence(N):

    spiral_indices = []
    x_min, x_max = 0, N - 1
    y_min, y_max = 0, N - 1

    while x_min <= x_max and y_min <= y_max:
        # Recorrer el borde superior (de izquierda a derecha)
        for i in range(x_min, x_max + 1):
            spiral_indices.append(y_min * N + i)
        y_min += 1

        # Recorrer el borde derecho (de arriba a abajo)
        for i in range(y_min, y_max + 1):
            spiral_indices.append(i * N + x_max)
        x_max -= 1

        # Recorrer el borde inferior (de derecha a izquierda)
        if y_min <= y_max:
            for i in range(x_max, x_min - 1, -1):
                spiral_indices.append(y_max * N + i)
            y_max -= 1

        # Recorrer el borde izquierdo (de abajo hacia arriba)
        if x_min <= x_max:
            for i in range(y_max, y_min - 1, -1):
                spiral_indices.append(i * N + x_min)
            x_min += 1

    return spiral_indices

def nilsson(state, spiral_sequence, N):

    p = 0
    # Convertir el estado a una lista en una única dimensión para compararla con la secuencia espiral.
    flat_state = [state[i][j] for i in range(N) for j in range(N)]

    # Recorrer la secuencia espiral y contar cuántas transiciones están fuera de orden
    for i in range(len(spiral_sequence) - 1):
        current_pos = spiral_sequence[i]  # Índice en la lista flat_state
        next_pos = spiral_sequence[i + 1]  # Índice en la lista flat_state

        # Asegúrate de comparar los valores correctos, ignorando el espacio en blanco (0)
        if flat_state[current_pos] != 0 and flat_state[next_pos] != 0:
            if flat_state[current_pos] != flat_state[next_pos] - 1:
                p += 1

    return p