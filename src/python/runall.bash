#!/usr/bin/env bash
# -*- coding: utf-8 -*-

flake8 --ignore=E111 *.py
cat ../selftest.ulisp | ./ulisp.py

