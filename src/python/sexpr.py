#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Chronian micro-lisp code to store s-exprs from input.
"""

from symbol_table import SymbolTable
from util import fatal_error

symbol_table = SymbolTable()


def eval(val):
  """ Eval any value, even if it might be nil.
  """
  if val is None:
    fatal_error("cannot eval nil")
  return val.eval()


class LispValue(object):
  """ Any kind of lisp value.  Used only as a parent class.
  """


class SExpr(LispValue):
  """ Holds any S-expression.  Used only as a parent class.
  """
  def __init__(self):
    pass

  def __repr__(self):
    return("<SExpr of unknown type>")

  def eval(self):
    fatal_error("eval not implemented for %s" % str(type(self)))


class List(SExpr):
  """ List cell ("cons" pair) for ulisp lists.
  """
  def __init__(self, left, right):
    self.left = left
    self.right = right

  def __repr__(self):
    rest = self
    result = []
    while (rest):
      left = rest.left.__repr__() if rest.left else "nil"
      result.append(left)
      rest = rest.right
    result = "(" + " ".join(result) + ")"
    return result

  def eval(self):
    return "TBA"


class Atom(SExpr):
  """ Atom superclass, used only as parent for subclasses.
  """
  def __init__(self):
    pass


class Symbol(Atom):
  """ An atom that holds a symbol (distinct from a string).
  """
  def __init__(self, name):
    self.symbol_number = symbol_table.find_or_add(name)

  def __repr__(self):
    return symbol_table.name(self.symbol_number)

  def eval(self):
    return "look it up in the env stack"


class String(Atom):
  """ An atom that holds a string.
  """
  def __init__(self, value):
    self.value = value

  def __repr__(self):
    return '"' + self.value + '"'  # fix this later to \-escape as needed

  def eval(self):
    return self


class Number(Atom):
  """ An atom that holds a number.  Used only as parent for subclasses.
  """
  def __init__(self):
    pass


class Integer(Number):
  """ An atom that holds an integer number.
  """
  def __init__(self, value):
    self.value = value

  def __repr__(self):
    return str(self.value)

  def eval(self):
    return self


class Float(Number):
  """ An atom that holds a floating point number.
  """
  def __init__(self, value):
    self.value = value

  def __repr__(self):
    return str(self.value)

  def eval(self):
    return self


class Boolean(Atom):
  """ An atom that holds a boolean value.
  """
  def __init__(self, value):
    self.value = value

  def __repr__(self):
    return "#t" if self.value else "#f"

  def eval(self):
    return self


class Quote(Atom):
  """ An atom that holds the symbol "'".  Used only for lexical scan.
  """
  def __init__(self):
    pass

  def __repr__(self):
    return "'"


class LeftParen(Atom):
  """ An atom that holds the symbol "(".  Used only for lexical scan.
  """
  def __init__(self):
    pass

  def __repr__(self):
    return "("


class RightParen(Atom):
  """ An atom that holds the symbol ")".  Used only for lexical scan.
  """
  def __init__(self):
    pass

  def __repr__(self):
    return ")"


class EOFToken(Atom):
  """ A special atom that indicates EOF on input.  Used only for lexical scan.
  """
  def __init__(self):
    pass

  def __repr__(self):
    return "EOF"
