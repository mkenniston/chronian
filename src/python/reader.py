#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Chronian micro-lisp code to read s-exprs from input.
"""

import sys
import re
from util import fatal_error
from sexpr import Integer, Float, String, Symbol, Boolean
from sexpr import Quote, LeftParen, RightParen


class Reader(object):
  """Read source code from stdin.
  """
  WHITE_SPACE_RE = re.compile(r"^[ \f\n\r\t\v]$")
  INTEGER_RE = re.compile(r"^[+-]?\d+$")
  FLOAT_RE = re.compile(r"[+-]?(\d+[.]?\d*|[.]\d+)(e[+-]\d+)?$")
  BREAK_RE = re.compile(r"^[ \f\n\r\t\v()';]$")
  line_buffer = []

  def read_next_line(self):
    """ Discard current line_buffer, and refill with next line from input.
    """
    self.line_buffer = sys.stdin.readline()
    self.line_buffer = list(self.line_buffer)
    self.line_buffer.reverse()

  def read_char(self):
    """ Return next unused character from the input, or "" if EOF.
    """
    if not self.line_buffer:
      self.read_next_line()
    if not self.line_buffer:
      return ""  # end of file
    return self.line_buffer.pop()

  def un_read_char(self, c):
    """ Undo the last read_char().
    """
    self.line_buffer.append(c)

  @staticmethod
  def parse_escaped_string_char(c):
    """ Given character "f", return "\f".
    """
    if not c:
      fatal_error("found EOF while reading a string")
    if c == "\\":
      result = "\\"
    elif c == '"':
      result = '"'
    elif c == "b":
      result = "\b"
    elif c == "f":
      result = "\f"
    elif c == "n":
      result = "\n"
    elif c == "r":
      result = "\r"
    elif c == "t":
      result = "\t"
    elif c == "v":
      result = "\v"
    else:
      fatal_error("unsupported escape sequence in string")
    return result

  def scan_string(self):
    """ Assume a double-quote has already been read.
        Read the rest of the string, including the closing double-quote,
        and return it as a lexeme.
    """
    string_chars = []
    c = self.read_char()
    while c != '"':
      if c == "\\":
        c = self.parse_escaped_string_char(self.read_char())
      string_chars.append(c)
      c = self.read_char()
    return String("".join(string_chars))

  def scan_word(self):
    """ Read one word (symbol, number, or boolean) from input, and return it.
    """
    word_chars = []
    c = self.read_char()
    while not self.BREAK_RE.match(c):
      word_chars.append(c)
      c = self.read_char()
    self.un_read_char(c)
    word = "".join(word_chars)
    if word == "#t":
      return Boolean(True)
    elif word == "#f":
      return Boolean(False)
    elif self.INTEGER_RE.match(word):
      return Integer(int(word))
    elif self.FLOAT_RE.match(word):
      return Float(float(word))
    else:
      return Symbol(word)

  def read_lexeme(self):
    """ Read one lexeme from input, and return it.
    """
    while True:
      c = self.read_char()
      while self.WHITE_SPACE_RE.match(c):
        c = self.read_char()
      if not c:
        return None  # EOF
      elif c == ";":
        self.read_next_line()  # discard comment
      elif c == "(":
        return LeftParen()
      elif c == ")":
        return RightParen()
      elif c == "'":
        return Quote()
      elif c == '"':
        return self.scan_string()
      else:
        self.un_read_char(c)
        return self.scan_word()
