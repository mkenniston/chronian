#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Chronian micro-lisp code to read s-exprs from input.
"""

import sys
import re
from util import error

LEX_INT = "int"
LEX_FLOAT = "float"
LEX_STRING = "string"
LEX_BOOLEAN = "boolean"
LEX_SYMBOL = "symbol"
LEX_LEFT_PAREN = "left_paren"
LEX_RIGHT_PAREN = "right_paren"
LEX_QUOTE = "quote"

WHITE_SPACE_RE = re.compile(r"^[ \f\n\r\t\v]$")
INTEGER_RE = re.compile(r"^[+-]?\d+$")
FLOAT_RE = re.compile(r"[+-]?(\d+[.]?\d*|[.]\d+)(e[+-]\d+)?$")
BREAK_RE = re.compile(r"^[ \f\n\r\t\v()';]$")


class Lexeme(object):
  """ Encapsulate one lexeme read by lexical scanner.
  """
  def __init__(self, lex_type, value):
    self.lex_type = lex_type
    self.value = value

  def __repr__(self):
    return "<Lexeme, type: " + self.lex_type + ", value: " + str(self.value) + ">"


class Reader(object):
  """Read source code from stdin.
  """
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
      error("found EOF while reading a string")
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
      error("unsupported escape sequence in string")
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
    return Lexeme(LEX_STRING, "".join(string_chars))


  def scan_word(self):
    """ Read one word (symbol, number, or boolean) from input, and return it.
    """
    word_chars = []
    c = self.read_char()
    while not BREAK_RE.match(c):
      word_chars.append(c)
      c = self.read_char()
    self.un_read_char(c)
    word = "".join(word_chars)
    if word == "#t":
      return Lexeme(LEX_BOOLEAN, True)
    elif word == "#f":
      return Lexeme(LEX_BOOLEAN, False)
    elif INTEGER_RE.match(word):
      return Lexeme(LEX_INT, int(word))
    elif FLOAT_RE.match(word):
      return Lexeme(LEX_FLOAT, float(word))
    else:
      return Lexeme(LEX_SYMBOL, word)


  def read_lexeme(self):
    """ Read one lexeme from input, and return it.
    """
    while True:
      c = self.read_char()
      while WHITE_SPACE_RE.match(c):
        c = self.read_char()
      if not c:
        return None  # EOF
      elif c == ";":
        self.read_next_line()  # discard comment
      elif c == "(":
        return Lexeme(LEX_LEFT_PAREN, None)
      elif c == ")":
        return Lexeme(LEX_RIGHT_PAREN, None)
      elif c == "'":
        return Lexeme(LEX_QUOTE, None)
      elif c == '"':
        return self.scan_string()
      else:
        self.un_read_char(c)
        return self.scan_word()
