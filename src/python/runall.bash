#!/usr/bin/env bash
# -*- coding: utf-8 -*-

pylint --rcfile=pylint.rc *.py
cat ../selftest.ulisp | ./ulisp.py

