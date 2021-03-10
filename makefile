
all: test-all

clean: clean-python clean-java clean-javascript clean-c

clean-python:
	cd src/python; make clean-python

clean-java:
	cd src/java; make clean-java

clean-javascript:
	cd src/javascript; make clean-javascript

clean-c:
	cd src/c; make clean-c

build-all: build-python build-java build-javascript build-c

build-python:
	cd src/python; make build-python

build-java:
	cd src/java; make build-java

build-javascript:
	cd src/javascript; make build-javascript

build-c:
	cd src/c; make build-c

test-all: test-python test-java test-javascript test-c

test-python:
	cd src/python; make test-python

test-java:
	cd src/java; make test-java

test-javascript:
	cd src/javascript; make test-javascript

test-c:
	cd src/c; make test-c
