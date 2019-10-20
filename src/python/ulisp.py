#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main program to run micro-lisp interpreter, which in turn
will run automated tests for Chronian.
"""

from util import fatal_error
from reader import Reader


def main():
  """ Do everything.
  """
  reader = Reader()
  lex = reader.read_lexeme()
  while lex:
    print("< %s, %s >" % (str(type(lex)), str(lex)))
    lex = reader.read_lexeme()
  fatal_error("Done!")


main()
