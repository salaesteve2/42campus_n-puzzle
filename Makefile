# NOT FINISHED; but working
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
        ./$(VENV)/bin/python3 main.py maps/3x3/3x3_zero_abajo Hamming -v

clean:
        rm -rf $(VENV)
        find . -type f -name '*.pyc' -delete

.PHONY: all venv run clean
