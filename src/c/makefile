
all: test-c

clean-c:
	rm -f ulisp

build-c: reader.h reader.c util.h util.c ulisp.c
	gcc -o ulisp reader.c util.c ulisp.c

test-c: build-c
	cat ../selftest.ulisp | ./ulisp

