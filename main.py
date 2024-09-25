import argparse
import sys
import os
import time
from colorama import Fore, Style, init
from src import maps, is_solvable, a_algorithm

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
        "Nilsson": "Nilsson",
        "Euclides": "Euclides"
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
    is_solvable.solvable(matrix_snale, matrix, size)

    if args.visualizer:
        print('Visualizer: ' + Fore.GREEN + 'True' + Style.RESET_ALL)
    else:
        print('Visualizer:' + Fore.RED + ' False' + Style.RESET_ALL)

    # Aplicar algoritmo solucion
    a_algorithm.a_algorithm(mode, args, matriz, matrix_snale, size, start_time)

if __name__ == "__main__":
    main()
