.PHONY: test run mac-app

test:
	python -m pip install -e .[test]
	PYTHONPATH=src python -m pytest

run:
	PYTHONPATH=src python -m checkbook_helper

mac-app:
	python -m pip install -e .[mac]
	python setup.py py2app
