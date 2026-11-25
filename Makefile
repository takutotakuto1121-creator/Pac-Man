VENV	= .venv
BIN		= $(VENV)/bin
PYTHON	= $(BIN)/python3
PIP		= $(BIN)/pip3
FLAKE8 	= $(BIN)/flake8
MYPY	= $(BIN)/mypy
FLAHS	= --warn-return-any\
		  --warn-unused-ignores\
		  --ignore-missing-imports\
		  --disallow-untyped-defs\
		  --check-untyped-defs


$(VENV):
	python3 -m venv $(VENV)

install: $(VENV)
	$(PIP) install -r requirements.txt

run: install
	$(PYTHON) pac-man.py config.json


debug:install
	$(PYTHON) -pdb pac-man.py config.json

clean:
	rm -rf __pycache__/
	rm -rf */__pycache/
	rm -rf .mypy_cache/
	rm -rf */.mypy_cache/

fclean:clean
	rm -rf $(VENV)

lint:install
	$(FLAKE8) --exclude=$(VENV) .
	$(MYPY) $(FLAGS) . --exclude $(VENV)

lint-strict: install
	$(FLAKE8) --exclude=$(VENV) .
	$(MYPY) --strict . --exclude $(VENV)
