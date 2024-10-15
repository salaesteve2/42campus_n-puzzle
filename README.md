# n-puzzle solver

**N-puzzle solver (School 42 Project)**
<br></br>

## About n-puzzle

**The n-puzzle** is a sliding puzzle having `n * n - 1` square tiles numbered from `1` to ` n * n - 1` in a frame that is `n` tiles high and `n` tiles wide, leaving one unoccupied tile position. Tiles in the same row or column of the open position can be moved by sliding them horizontally or vertically, respectively. The goal of the puzzle is to place the tiles in spiral order. [[Wiki]](https://en.wikipedia.org/wiki/15_puzzle)


### How to use

1. Install required packages:

	```
	pip install --no-cache-dir -r requeriments.txt
	```
2. Run n-puzzle solver:

	```
	python main.py file heuristic_function [-g] [-v] [-c] [-n]

	positional arguments:
	  heuristic_function  specifies heuristic function
	  file                file, which contains the initial grid

	optional arguments:
	  -g                  enable only greedy search
	  -v                  use visualizer
 	  -c                  enable only uniform cost
      -n                  use a non-admisible heuristic
 
	```

## Heuristics

- **Admissible** - guarantees optimal solution [[Wiki]](https://en.wikipedia.org/wiki/Admissible_heuristic)
	- Manhattan distance
	- Hamming
	- Number of tiles out of row + Number of tiles out of column 
<br></br>
- **Non-admissible** - A non-admissible heuristic may overestimate the cost of reaching the goal. It may or may not result in an optimal solution. However, the advantage is that sometimes, a non-admissible heuristic expands much fewer nodes. Thus, the total cost (= search cost + path cost) may actually be lower than an optimal solution using an admissible heuristic.
	- Nilsson's sequence score <br></br>

## Additional tools

- **Puzzles generator**. Usage:

	1. Run generator:

		```
		python npuzzle-gen.py [-h] [-s] [-u] [-i ITERATIONS] size

		positional arguments:
		  size                  Size of the puzzle's side. Must be >3.

		optional arguments:
		  -h, --help            show this help message and exit
		  -s, --solvable        Forces generation of a solvable puzzle. Overrides -u.
		  -u, --unsolvable      Forces generation of an unsolvable puzzle
		  -i ITERATIONS, --iterations ITERATIONS
		                        Number of passes
		```



SALUS PRUEBA ESTE MAKE (pero dale a edit para copiarlo que se ve raro aqui):


# define the name of the virtual environment directory
VENV := venv

# default target, when make executed without arguments
all: venv

$(VENV)/bin/activate:
        python3 -m venv $(VENV)
        ./$(VENV)/bin/pip install colorama
        ./$(VENV)/bin/pip install pygame
        ./$(VENV)/bin/pip install termcolor

python3_check:
        python3 -V 2>/dev/null || (echo "python installin" && install_python3)

install_python3:
        curl -L0 https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe

# venv is a shortcut target
venv: $(VENV)/bin/activate python3_check

run: venv
        @read -p "Introduce el archivo: " filename; \
        read -p "Introduce el método: " method; \
        read -p "Introduce modos: " mode; \
        if [ -z "$$filename" ] || [ -z "$$method" ]; then \
                echo "Parámetros vacíos"; \
        else \
                if [ -z "$$mode" ]; then \
                        ./$(VENV)/bin/python3 main.py $$filename $$method; \
                else \
                        ./$(VENV)/bin/python3 main.py $$filename $$method $$mode; \
                fi; \
        fi

clean:
        rm -rf $(VENV)
        find . -type f -name '*.pyc' -delete

.PHONY: all venv run clean
