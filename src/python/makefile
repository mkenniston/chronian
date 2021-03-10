
all: test-python

clean-python:
	rm -f *.pyc

build-python:
	flake8 --ignore=E111,E114,W504 *.py

test-python: build-python
	cat ../selftest.ulisp | ./ulisp.py

