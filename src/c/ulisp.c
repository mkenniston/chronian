// -*- coding: utf-8 -*-

#include "reader.h"

void main(char **argv) {
  Reader *reader = Reader_new();
  Lexeme *lex = Reader_read_lexeme(reader);
  while (lex) {
    Lexeme_print(lex);
    lex = Reader_read_lexeme(reader);
  }
  error("Done!");
}

