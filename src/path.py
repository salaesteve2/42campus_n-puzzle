from colorama import Fore, Style, init

def path(route, actual_list):
    path = [actual_list]
    while actual_list in route:
        actual_list = route[actual_list]
        path.append(actual_list)
    path.reverse()
    print('Total number of moves: ' + Fore.GREEN + str(len(path)) + Style.RESET_ALL)
    print("Sequence of moves:")
    for step in path:
        for row in step:
            print(Fore.LIGHTBLACK_EX + str(row) + Style.RESET_ALL)
        print()
    return path

def position_zero(size, state):
    for i in range(size):
        for j in range(size):
            if state[i][j] == 0:
                return i, j

def generate_next(size, state):
    filzero, colzero = position_zero(size, state)
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    successors = []

    for dr, dc in directions:
        fil, col = filzero + dr, colzero + dc
        if 0 <= fil < size and 0 <= col < size:
            # Crea una copia del estado original
            new_state = [row[:] for row in state]  # Usar slicing para copiar
            # Intercambia el cero con el número en la nueva posición
            new_state[filzero][colzero], new_state[fil][col] = new_state[fil][col], new_state[filzero][colzero]
            successors.append(new_state)

    return successors