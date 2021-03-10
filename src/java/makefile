
V0 = com/chronian/v0

all: test-java

clean-java:
	rm -f $(V0)/*.class

build-java:
	javac $(V0)/*.java

test-java: build-java
	cat ../selftest.ulisp | java $(V0)/ULisp

