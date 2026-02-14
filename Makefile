.PHONY: test run

test:
	python -m pip install -e .[test]
	PYTHONPATH=src python -m pytest

run:
	PYTHONPATH=src python -m checkbook_helper
