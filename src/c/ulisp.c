// -*- coding: utf-8 -*-

#include <stdlib.h>
#include <stdio.h>
#include "reader.h"
#include "util.h"

void main(char **argv) {
  Reader *reader = Reader_new();
  Lexeme *lex = Reader_read_lexeme(reader);
  while (lex) {
    Lexeme_print(lex);
    lex = Reader_read_lexeme(reader);
  }
  printf("Done!\n");
  exit(0);
}

