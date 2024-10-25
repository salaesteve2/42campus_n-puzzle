from src import path, visualizer
from colorama import Fore, Style
import time
import sys

def solution(open_set, visited, start_time, route, actual_list, size, args):
    print(Fore.GREEN + "Solution found" + Style.RESET_ALL)
    print('Total number of states selected (time complexity): ' + Fore.GREEN + str(
        len(open_set)) + Style.RESET_ALL)  # cantidad de nodos a lo largo de la ejecucion
    print('Total number of states in memory (space complexity): ' + Fore.GREEN + str(
        len(visited)) + Style.RESET_ALL)  # #cantidad de nodos que fueron visitados y alamacenados en el momento de encontrar la solucion
    end_time = time.time()
    execution_time = end_time - start_time
    print('Execution time: ' + Fore.GREEN + f"{execution_time:.5f}" + ' seconds' + Style.RESET_ALL)
    path1 = path.path(route, actual_list)

    # Llamar al visualizador
    if args.visualizer:
        visualizer.visualizer_solution(path1, size)

    sys.exit(0)