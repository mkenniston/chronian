#!/usr/bin/env bash
# -*- coding: utf-8 -*-

rm -f ulisp
gcc -o ulisp reader.c ulisp.c
cat ../selftest.ulisp | ./ulisp

