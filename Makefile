VENV	= .venv
bIN		= $(VENV)/bin
PYTHON	= $(BIN)/python3
PIP		= $(BIN)/pip
FLAKE8 	= $(BIN)/flake8
MYPY	= $(BIN)/mypy


$(VENV):
	python3 -m venv $(VENV)

install: $(VENV)
	$(PIP) install -r requirements.txt

run: 
