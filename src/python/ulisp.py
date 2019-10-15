#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re

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

line_buffer = []


class Lexeme:
  def __init__(self, type, value):
    self.type = type
    self.value = value

  def __repr__(self):
    return "<Lexeme, type: " + self.type + ", value: " + str(self.value) + ">"


def error(msg):
  print msg
  exit(1)
 

def read_next_line():
  """ Discard current line_buffer, and refill with next line from input.
  """
  global line_buffer
  line_buffer = sys.stdin.readline()
  line_buffer = list(line_buffer)
  line_buffer.reverse()


def get_char():
  """ Return next unused character from the input, or "" if EOF.
  """
  global line_buffer
  if not line_buffer:
    read_next_line()
  if not line_buffer:
    return ""  # end of file
  return line_buffer.pop()


def un_get_char(c):
  """ Undo the last get_char().
  """
  global line_buffer
  line_buffer.append(c)


def scan_string():
  """ Assume a double-quote has already been read.
      Read the rest of the string, including the closing double-quote,
      and return it as a lexeme.
  """
  s = []
  c = get_char()
  while c != '"':
    if c == "\\":
      c = get_char()
      if not c: error("found EOF while reading a string")
      elif c == "\\": s.append("\\")
      elif c == '"': s.append('"')
      elif c == "b": s.append("\b")
      elif c == "f": s.append("\f")
      elif c == "n": s.append("\n")
      elif c == "r": s.append("\r")
      elif c == "t": s.append("\t")
      elif c == "v": s.append("\v")
      else: error("unsupported escape sequence in string")
    else:
      s.append(c)
    c = get_char()
  return Lexeme(LEX_STRING, "".join(s))


def scan_word():
  s = []
  c = get_char()
  while not BREAK_RE.match(c):
    s.append(c)
    c = get_char()
  un_get_char(c)
  s = "".join(s)
  if s == "#t": return Lexeme(LEX_BOOLEAN, True)
  if s == "#f": return Lexeme(LEX_BOOLEAN, False)
  if INTEGER_RE.match(s): return Lexeme(LEX_INT, int(s))
  if FLOAT_RE.match(s): return Lexeme(LEX_FLOAT, float(s))
  return Lexeme(LEX_SYMBOL, s)


def get_lexeme():
  while True:
    c = get_char()
    while WHITE_SPACE_RE.match(c):
      c = get_char()
    if not c:
      return None  # EOF
    elif c == ";":
      read_next_line()  # discard comment
      next
    elif c == "(":
      return Lexeme(LEX_LEFT_PAREN, None)
    elif c == ")":
      return Lexeme(LEX_RIGHT_PAREN, None)
    elif c == "'":
      return Lexeme(LEX_QUOTE, None)
    elif c == '"':
      return scan_string()
    else:
      un_get_char(c)
      return scan_word()


lex = get_lexeme()
while lex:
  print lex
  lex = get_lexeme()

error("Done!")

