#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main program to run micro-lisp interpreter, which in turn
will run automated tests for Chronian.
"""

from util import fatal_error
from reader import Reader
from sexpr import EOFToken


def dump_lexemes(reader):
  lex = reader.read_lexeme()
  while not isinstance(lex, EOFToken):
    print("< %s, %s >" % (str(type(lex)), str(lex)))
    lex = reader.read_lexeme()


def dump_sexprs(reader):
  exp = reader.read_sexpr()
  print("< %s >" % (exp if exp else "nil"))
  while not isinstance(exp, EOFToken):
    exp = reader.read_sexpr()
    print("< %s >" % (exp if exp else "nil"))


def main():
  """ Do everything.
  """
  reader = Reader()
  # dump_lexemes(reader)
  dump_sexprs(reader)
  fatal_error("Done!")


main()
