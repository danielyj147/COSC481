VENV := ../.venv
PYTHON := $(VENV)/bin/python

.PHONY: run clean

run:
	$(PYTHON) main.py

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
