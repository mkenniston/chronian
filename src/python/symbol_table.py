#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Utility routines for Chronian micro-lisp interpreter.
"""

from util import fatal_error


class SymbolTable:
  """ Table of symbol names, so we can compare symbols without doing
      full string comparisons.
  """

  TABLE_SIZE = 1000

  def __init__(self):
    self.table = [None] * self.TABLE_SIZE
    self.table[0] = "nil"
    self.next = 1

  def find(self, name):
    """ Look up a name in the symbol table, and return the unique integer
        assigned to that name.  Return "None" if the name is not in the table.
    """
    for i in range(0, self.next):
      if self.table[i] == name:
        return i
    return None

  def find_or_add(self, name):
    """ Look up a name in the symbol table, but if it is not found then add it.
    """
    for i in range(0, self.next):
      if self.table[i] == name:
        return i
    if self.next >= self.TABLE_SIZE:
      fatal_error("symbol table overflow")
    self.table[self.next] = name
    result = self.next
    self.next += 1
    return result

  def name(self, symbol_number):
    return self.table[symbol_number]
