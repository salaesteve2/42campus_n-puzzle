from colorama import Fore, Style, init

def camino_recorrido(recorrido, lista_actual):
    camino = [lista_actual]
    while lista_actual in recorrido:
        lista_actual = recorrido[lista_actual]
        camino.append(lista_actual)
    camino.reverse()
    print('Total number of moves: ' + Fore.GREEN + str(len(camino)) + Style.RESET_ALL)
    print("Sequence of moves:")
    for step in camino:
        for row in step:
            print(Fore.LIGHTBLACK_EX + str(row) + Style.RESET_ALL)
        print()
    return camino

def posicion_zero(size, estado):
    for i in range(size):
        for j in range(size):
            if estado[i][j] == 0:
                return i, j

def generar_sucesores(size, estado):
    filzero, colzero = posicion_zero(size, estado)
    direcciones = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    sucesores = []

    for dr, dc in direcciones:
        fil, col = filzero + dr, colzero + dc
        if 0 <= fil < size and 0 <= col < size:
            # Crea una copia del estado original
            estado_nuevo = [row[:] for row in estado]  # Usar slicing para copiar
            # Intercambia el cero con el número en la nueva posición
            estado_nuevo[filzero][colzero], estado_nuevo[fil][col] = estado_nuevo[fil][col], estado_nuevo[filzero][colzero]
            sucesores.append(estado_nuevo)

    return sucesores