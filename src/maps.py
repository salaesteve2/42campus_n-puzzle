import sys
from colorama import Fore, Style, init

def generate_snail(n):
    # Crear una matriz vacía de tamaño n x n
    matriz = [[0] * n for _ in range(n)]

    # Inicializar los límites de la matriz
    izquierda, derecha = 0, n - 1
    arriba, abajo = 0, n - 1
    numero = 1

    while izquierda <= derecha and arriba <= abajo:
        # Llenar la fila superior de izquierda a derecha
        for j in range(izquierda, derecha + 1):
            matriz[arriba][j] = numero
            numero += 1
        arriba += 1

        # Llenar la columna derecha de arriba a abajo
        for i in range(arriba, abajo + 1):
            matriz[i][derecha] = numero
            numero += 1
        derecha -= 1

        # Llenar la fila inferior de derecha a izquierda, si aún hay filas
        if arriba <= abajo:
            for j in range(derecha, izquierda - 1, -1):
                matriz[abajo][j] = numero
                numero += 1
            abajo -= 1

        # Llenar la columna izquierda de abajo a arriba, si aún hay columnas
        if izquierda <= derecha:
            for i in range(abajo, arriba - 1, -1):
                matriz[i][izquierda] = numero
                numero += 1
            izquierda += 1

    max_num = n * n  # El número más grande en una matriz n x n es n*n
    for i in range(n):
        for j in range(n):
            if matriz[i][j] == max_num:
                matriz[i][j] = 0
                break

    return matriz

def read_map(map_matrix):
    lines = []
    with open(map_matrix, 'r') as file:
        for line in file:
            if '#' in line:
                position = line.find('#')
                line = line[:position]
            if any(caracter.isdigit() for caracter in line):
                lines.append(line.strip())
    return lines

def process_map(lines):
    # rellenar en una lista
    matriz = []
    size1 = 0
    for line in lines:
        # verificacion que no haya letras
        if any(isinstance(i, str) and i.isalpha() for i in line):
            print(Fore.RED + "Error. The map is not correct." + Style.RESET_ALL)
            sys.exit(1)
        if len(line) == 1:
            size1 = int(line.strip())
            print("Size: " + Fore.LIGHTMAGENTA_EX + str(size1) + ' * ' + str(size1) + Style.RESET_ALL)
        else:
            numbers = list(map(int, line.split()))
            matriz.append(numbers)
    return matriz, size1