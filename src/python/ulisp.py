#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main program to run micro-lisp interpreter, which in turn
will run automated tests for Chronian.
"""

from util import error
from reader import Reader


def main():
  """ Do everything.
  """
  reader = Reader()
  lex = reader.read_lexeme()
  while lex:
    print(lex)
    lex = reader.read_lexeme()
  error("Done!")


main()
