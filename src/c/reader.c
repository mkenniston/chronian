// -*- coding: utf-8 -*-

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <regex.h>

#include "reader.h"

const char* const LEX_INT = "int";
const char* const LEX_FLOAT = "float";
const char* const LEX_STRING = "string";
const char* const LEX_BOOLEAN = "boolean";
const char* const LEX_SYMBOL = "symbol";
const char* const LEX_LEFT_PAREN = "left_paren";
const char* const LEX_RIGHT_PAREN = "right_paren";
const char* const LEX_QUOTE = "quote";

regex_t WHITE_SPACE_RE;
regex_t INTEGER_RE;
regex_t FLOAT_RE;
regex_t BREAK_RE;


void error(char *msg) {
  printf("%s\n", msg);
  exit(1);
}

void append_char(char **buf, char c) {
  size_t len = *buf ? strlen(*buf) : 0;
  char *tmp = malloc(len + 1 + 1);
  if (*buf) { strcpy(tmp, *buf); }
  tmp[len] = c;
  tmp[len+1] = '\0';
  free(*buf);
  *buf = tmp;
}


void Lexeme_print(Lexeme *pThis) {
  if (strcmp(pThis->type, LEX_INT) == 0) {
    printf("<Lexeme, type = %s, value = %d>\n", pThis->type, pThis->i_value);
  } else if (strcmp(pThis->type, LEX_FLOAT) == 0) {
    printf("<Lexeme, type = %s, value = %f>\n", pThis->type, pThis->f_value);
  } else if (strcmp(pThis->type, LEX_STRING) == 0) {
    printf("<Lexeme, type = %s, value = %s>\n", pThis->type, pThis->s_value);
  } else if (strcmp(pThis->type, LEX_BOOLEAN) == 0) {
    printf("<Lexeme, type = %s, value = %s>\n", pThis->type,
      pThis->f_value ? "true" : "false");
  } else if (strcmp(pThis->type, LEX_SYMBOL) == 0) {
    printf("<Lexeme, type = %s, value = %s>\n", pThis->type, pThis->s_value);
  } else if (strcmp(pThis->type, LEX_LEFT_PAREN) == 0) {
    printf("<Lexeme, type = %s>\n", pThis->type);
  } else if (strcmp(pThis->type, LEX_RIGHT_PAREN) == 0) {
    printf("<Lexeme, type = %s>\n", pThis->type);
  } else if (strcmp(pThis->type, LEX_QUOTE) == 0) {
    printf("<Lexeme, type = %s>\n", pThis->type);
  }
}

Lexeme* Lexeme_new(const char* const type) {
  Lexeme* result = malloc(sizeof(Lexeme));
  result->type = type;
  return result;
}

Reader* Reader_new() {
  int flags = REG_EXTENDED | REG_NOSUB;
  if (regcomp(&WHITE_SPACE_RE, "^[ \f\n\r\t\v]$", flags) ||
      regcomp(&INTEGER_RE, "^[+-]?[0-9]+$", flags) ||
      regcomp(&FLOAT_RE, "[+-]?([0-9]+[.]?[0-9]*|[.][0-9]+)(e[+-][0-9]+)?$", flags) ||
      regcomp(&BREAK_RE, "^[ \f\n\r\t\v()';]$", flags)) {
    error("failed to compile a regex");
  }

  Reader* pThis = malloc(sizeof(Reader));
  pThis->line_buffer = NULL;
  pThis->cur_char = NULL;
  return pThis;
}

void Reader_read_next_line(Reader *pThis) {
  size_t size;
  free(pThis->line_buffer);
  pThis->line_buffer = NULL;
  if (getline(&(pThis->line_buffer), &size, stdin) == -1) {
    pThis->line_buffer = NULL;
  } else {
    pThis->cur_char = pThis->line_buffer;
  }
}

char Reader_read_char(Reader *pThis) {
  if (pThis->line_buffer == NULL || *(pThis->cur_char) == 0) {
    Reader_read_next_line(pThis);
  }
  if (pThis->line_buffer == NULL) {
    return '\0';  // end of file
  }
  return *(pThis->cur_char++);
}

void Reader_un_read_char(Reader *pThis, char c) {
  *(--pThis->cur_char) = c;
}

Lexeme* Reader_scan_string(Reader *pThis) {
  char *s = NULL;
  char c = Reader_read_char(pThis);
  while (c != '"') {
    if (c == '\\') {
      c = Reader_read_char(pThis);
      if (! c) {
        error("found EOF while reading a string");
      } else if (c == '\\') {
        append_char(&s, '\\');
      } else if (c == '"') {
        append_char(&s, '"');
      } else if (c == 'b') {
        append_char(&s, '\b');
      } else if (c == 'f') {
        append_char(&s, '\f');
      } else if (c == 'n') {
        append_char(&s, '\n');
      } else if (c == 'r') {
        append_char(&s, '\r');
      } else if (c == 't') {
        append_char(&s, '\t');
      } else if (c == 'v') {
        append_char(&s, '\v');
      } else {
        error("unsupported escape sequence in string");
      }
    } else {
      append_char(&s, c);
    }
    c = Reader_read_char(pThis);
  }
  Lexeme *lex = Lexeme_new(LEX_STRING);
  lex->s_value = s;
  return lex;
}

Lexeme* Reader_scan_word(Reader *pThis) {
  char *s = NULL;
  char c[2];
  c[1] = '\0';
  c[0] = Reader_read_char(pThis);
  while (regexec(&BREAK_RE, c, 0, NULL, 0)) {
    append_char(&s, c[0]);
    c[0] = Reader_read_char(pThis);
  }
  Reader_un_read_char(pThis, c[0]);
  if (strcmp(s, "#t") == 0) {
    Lexeme *lex = Lexeme_new(LEX_BOOLEAN);
    lex->b_value = true;
    return lex;
  }
  if (strcmp(s, "#f") == 0) {
    Lexeme *lex = Lexeme_new(LEX_BOOLEAN);
    lex->b_value = false;
    return lex;
  }
  if (! regexec(&INTEGER_RE, s, 0, NULL, 0)) {
    Lexeme *lex = Lexeme_new(LEX_INT);
    lex->i_value = atoi(s);
    return lex;
  }
  if (! regexec(&FLOAT_RE, s, 0, NULL, 0)) {
    Lexeme *lex = Lexeme_new(LEX_FLOAT);
    lex->f_value = atof(s);
    return lex;
  }
  Lexeme *lex = Lexeme_new(LEX_SYMBOL);
  lex->s_value = s;
  return lex;
}

Lexeme* Reader_read_lexeme(Reader *pThis) {
  while (true) {
    char c[2];
    c[1] = '\0';
    c[0] = Reader_read_char(pThis);
    int rv = regexec(&WHITE_SPACE_RE, c, 0, NULL, 0);
    while (! regexec(&WHITE_SPACE_RE, c, 0, NULL, 0)) {
      c[0] = Reader_read_char(pThis);
    }
    if (! c[0]) {
      return NULL;  // EOF
    }
    if (c[0] == ';') {
      Reader_read_next_line(pThis);
      continue;
    }
    if (c[0] == '(') {
      return Lexeme_new(LEX_LEFT_PAREN);
    } else if (c[0] == ')') {
      return Lexeme_new(LEX_RIGHT_PAREN);
    } else if (c[0] == '\'') {
      return Lexeme_new(LEX_QUOTE);
    } else if (c[0] == '"') {
      return Reader_scan_string(pThis);
    }
    Reader_un_read_char(pThis, c[0]);
    return Reader_scan_word(pThis);
  }
}

