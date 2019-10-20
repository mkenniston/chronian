#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Utility routines for Chronian micro-lisp interpreter.
"""

# import sys


def fatal_error(msg):
  """ Display an error message, and abort the program.
  """
  print(msg)
  exit(1)
