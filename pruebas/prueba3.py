import random
import heapq


def create_spiral_matrix(n):
    """Crea una matriz n x n en forma de espiral."""
    matrix = [[0] * n for _ in range(n)]
    left, right = 0, n - 1
    top, bottom = 0, n - 1
    num = 1

    while left <= right and top <= bottom:
        for i in range(left, right + 1):
            matrix[top][i] = num
            num += 1
        top += 1

        for i in range(top, bottom + 1):
            matrix[i][right] = num
            num += 1
        right -= 1

        if top <= bottom:
            for i in range(right, left - 1, -1):
                matrix[bottom][i] = num
                num += 1
            bottom -= 1

        if left <= right:
            for i in range(bottom, top - 1, -1):
                matrix[i][left] = num
                num += 1
            left += 1

    return matrix


def flatten_matrix(matrix):
    """Convierte una matriz 2D en una lista 1D."""
    return [item for row in matrix for item in row]


def is_solvable(board):
    """Verifica si el rompecabezas es solucionable."""
    inversions = 0
    flat_board = [tile for tile in board if tile != 0]

    for i in range(len(flat_board)):
        for j in range(i + 1, len(flat_board)):
            if flat_board[i] > flat_board[j]:
                inversions += 1

    return inversions % 2 == 0


def shuffle_board(board):
    """Desordena el tablero de forma válida."""
    while True:
        random.shuffle(board)
        if is_solvable(board):
            return board


# Crear el estado objetivo en forma de caracol
target_spiral_matrix = create_spiral_matrix(4)
target_board = flatten_matrix(target_spiral_matrix)
target_board[-1] = 0  # Colocar el espacio vacío en la última posición

# Estado inicial desordenado
initial_board = shuffle_board([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0])

print("Estado inicial:")
for i in range(4):
    print(initial_board[i * 4:(i + 1) * 4])

# Comprobar si es solucionable
if not is_solvable(initial_board):
    print("El estado inicial no es solucionable.")
else:
    class PuzzleState:
        def __init__(self, board, empty_tile, moves=0, previous=None):
            self.board = board
            self.empty_tile = empty_tile
            self.moves = moves
            self.previous = previous
            self.heuristic = self.calculate_heuristic()

        def calculate_heuristic(self):
            """Heurística: número de piezas fuera de lugar."""
            return sum(1 for i in range(16) if self.board[i] != target_board[i])

        def is_goal(self):
            return self.board == target_board

        def get_neighbors(self):
            neighbors = []
            x, y = divmod(self.empty_tile, 4)
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            for dx, dy in directions:
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < 4 and 0 <= new_y < 4:
                    new_empty_tile = new_x * 4 + new_y
                    new_board = self.board[:]
                    new_board[self.empty_tile], new_board[new_empty_tile] = new_board[new_empty_tile], new_board[
                        self.empty_tile]
                    neighbors.append(PuzzleState(new_board, new_empty_tile, self.moves + 1, self))
            return neighbors

        def __lt__(self, other):
            return (self.moves + self.heuristic) < (other.moves + other.heuristic)


    def a_star(initial_board):
        initial_empty_tile = initial_board.index(0)
        initial_state = PuzzleState(initial_board, initial_empty_tile)
        open_set = []
        heapq.heappush(open_set, (initial_state.heuristic, initial_state))
        closed_set = set()

        while open_set:
            current_heuristic, current_state = heapq.heappop(open_set)

            if current_state.is_goal():
                return reconstruct_path(current_state)

            closed_set.add(tuple(current_state.board))

            for neighbor in current_state.get_neighbors():
                if tuple(neighbor.board) not in closed_set:
                    heapq.heappush(open_set, (neighbor.moves + neighbor.heuristic, neighbor))

            # Mensaje de depuración
            if len(closed_set) % 1000 == 0:
                print(f"Explorados: {len(closed_set)} estados.")

        return None  # No se encontró solución


    def reconstruct_path(state):
        path = []
        while state:
            path.append(state.board)
            state = state.previous
        return path[::-1]


    # Ejecutar el algoritmo A* en el estado inicial
    solution = a_star(initial_board)
    if solution:
        print("\nSolución encontrada:")
        for step in solution:
            print(step)
    else:
        print("No se encontró solución.")
