#!/usr/bin/env bash
# -*- coding: utf-8 -*-

gcc -o ulisp ulisp.c
cat ../selftest.ulisp | ./ulisp

