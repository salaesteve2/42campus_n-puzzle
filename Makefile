# define the name of the virtual environment directory
VENV := venv

# default target, when make executed without arguments
all: venv

$(VENV)/bin/activate: requirements.txt
	 python3 -m venv $(VENV)
	 ./$(VENV)/bin/pip install colorama
	 ./$(VENV)/bin/pip install pygame
	 ./$(VENV)/bin/pip install termcolor

# venv is a shortcut target
venv: $(VENV)/bin/activate

run: venv
	@read -p "Introduce el archivo: " filename; \
	 read -p "Introduce el método: " method; \
	 read -p "Introduce modos: " mode; \
	 ./$(VENV)/bin/python3 main.py $$filename $$method $$mode

clean:
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete

.PHONY: all venv run clean
