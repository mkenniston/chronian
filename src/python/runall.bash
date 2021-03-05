#!/usr/bin/env bash
# -*- coding: utf-8 -*-

flake8 --ignore=E111,E114,W504 *.py
cat ../selftest.ulisp | ./ulisp.py

