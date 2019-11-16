all: venv

PYBIN=venv/bin
PYTHON=$(PYBIN)/python
PIP=$(PYBIN)/pip

venv:
	python3 -m venv venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PIP) install -e .
