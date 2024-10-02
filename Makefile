# define the name of the virtual environment directory
VENV := venv

# default target, when make executed without arguments
all: venv

$(VENV)/bin/activate:
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
	 if [ -z "$$mode" ]; then \
             ./$(VENV)/bin/python3 main.py $$filename $$method; \
         else \
             ./$(VENV)/bin/python3 main.py $$filename $$method $$mode; \
         fi

clean:
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete

.PHONY: all venv run clean
