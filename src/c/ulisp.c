// -*- coding: utf-8 -*-

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <regex.h>

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


char* line_buffer = NULL;
char* cur_char = NULL;

typedef struct {
  const char* type;
  union {
    char* s_value;
    int i_value;
    float f_value;
    bool b_value;
  };
} Lexeme;

void print_lexeme(Lexeme *lex) {
  if (strcmp((*lex).type, LEX_INT) == 0) {
    printf("<Lexeme, type = %s, value = %d>\n", (*lex).type, (*lex).i_value);
  } else if (strcmp((*lex).type, LEX_FLOAT) == 0) {
    printf("<Lexeme, type = %s, value = %f>\n", (*lex).type, (*lex).f_value);
  } else if (strcmp((*lex).type, LEX_STRING) == 0) {
    printf("<Lexeme, type = %s, value = %s>\n", (*lex).type, (*lex).s_value);
  } else if (strcmp((*lex).type, LEX_BOOLEAN) == 0) {
    printf("<Lexeme, type = %s, value = %s>\n", (*lex).type,
      (*lex).f_value ? "true" : "false");
  } else if (strcmp((*lex).type, LEX_SYMBOL) == 0) {
    printf("<Lexeme, type = %s, value = %s>\n", (*lex).type, (*lex).s_value);
  } else if (strcmp((*lex).type, LEX_LEFT_PAREN) == 0) {
    printf("<Lexeme, type = %s>\n", (*lex).type);
  } else if (strcmp((*lex).type, LEX_RIGHT_PAREN) == 0) {
    printf("<Lexeme, type = %s>\n", (*lex).type);
  } else if (strcmp((*lex).type, LEX_QUOTE) == 0) {
    printf("<Lexeme, type = %s>\n", (*lex).type);
  }
}

Lexeme* new_Lexeme(const char* const type) {
  Lexeme* result = malloc(sizeof(Lexeme));
  (*result).type = type;
  return result;
}

void error(char *msg) {
  printf("%s\n", msg);
  exit(1);
}

void init_regex() {
  int flags = REG_EXTENDED | REG_NOSUB;
  if (regcomp(&WHITE_SPACE_RE, "^[ \f\n\r\t\v]$", flags) ||
      regcomp(&INTEGER_RE, "^[+-]?[0-9]+$", flags) ||
      regcomp(&FLOAT_RE, "[+-]?([0-9]+[.]?[0-9]*|[.][0-9]+)(e[+-][0-9]+)?$", flags) ||
      regcomp(&BREAK_RE, "^[ \f\n\r\t\v()';]$", flags)) {
    error("failed to compile a regex");
  }
}

void read_next_line() {
  size_t size;
  free(line_buffer);
  line_buffer = NULL;
  if (getline(&line_buffer, &size, stdin) == -1) {
    line_buffer = NULL;
  } else {
    cur_char = line_buffer;
  }
  // fprintf(stderr, "TRACE Q, line = <%s>\n", line_buffer);
}

char get_char() {
  if (line_buffer == NULL || *cur_char == 0) {
    read_next_line();
  }
  if (line_buffer == NULL) {
    return '\0';  // end of file
  }
  return *(cur_char++);
}

void un_get_char(char c) {
  *(--cur_char) = c;
}

void append_char(char **buf, char c) {
  // fprintf(stderr, "trace +A: <%c>, <%d>\n", c, *buf);
  size_t len = *buf ? strlen(*buf) : 0;
  // fprintf(stderr, "trace +B: %d\n", len);
  char *tmp = malloc(len + 1 + 1);
  if (*buf) { strcpy(tmp, *buf); }
  // fprintf(stderr, "trace +C\n");
  tmp[len] = c;
  tmp[len+1] = '\0';
  // fprintf(stderr, "trace +D: <%d>\n", *buf);
  free(*buf);
  // fprintf(stderr, "trace +E\n");
  *buf = tmp;
}

Lexeme* scan_string() {
  char *s = NULL;
  char c = get_char();
  while (c != '"') {
    if (c == '\\') {
      c = get_char();
      if (! c) { error("found EOF while reading a string"); }
      else if (c == '\\') { append_char(&s, '\\'); }
      else if (c == '"') { append_char(&s, '"'); }
      else if (c == 'b') { append_char(&s, '\b'); }
      else if (c == 'f') { append_char(&s, '\f'); }
      else if (c == 'n') { append_char(&s, '\n'); }
      else if (c == 'r') { append_char(&s, '\r'); }
      else if (c == 't') { append_char(&s, '\t'); }
      else if (c == 'v') { append_char(&s, '\v'); }
      else { error("unsupported escape sequence in string"); }
    } else {
      append_char(&s, c);
    }
    c = get_char();
  }
  Lexeme *lex = new_Lexeme(LEX_STRING);
  (*lex).s_value = s;
  return lex;
}

Lexeme* scan_word() {
  // fprintf(stderr, "trace S\n");
  char *s = NULL;
  char c[2];
  c[1] = '\0';
  c[0] = get_char();
  // fprintf(stderr, "trace T\n");
  while (regexec(&BREAK_RE, c, 0, NULL, 0)) {
    // fprintf(stderr, "trace U\n");
    append_char(&s, c[0]);
    c[0] = get_char();
    // fprintf(stderr, "trace V\n");
  }
  // fprintf(stderr, "trace W: <%c>\n", c[0]);
  un_get_char(c[0]);
  if (strcmp(s, "#t") == 0) {
    Lexeme *lex = new_Lexeme(LEX_BOOLEAN);
    (*lex).b_value = true;
    return lex;
  }
  if (strcmp(s, "#f") == 0) {
    Lexeme *lex = new_Lexeme(LEX_BOOLEAN);
    (*lex).b_value = false;
    return lex;
  }
  if (! regexec(&INTEGER_RE, s, 0, NULL, 0)) {
    fprintf(stderr, "trace Z\n");
    Lexeme *lex = new_Lexeme(LEX_INT);
    (*lex).i_value = atoi(s);
    return lex;
  }
  if (! regexec(&FLOAT_RE, s, 0, NULL, 0)) {
    Lexeme *lex = new_Lexeme(LEX_FLOAT);
    (*lex).f_value = atof(s);
    return lex;
  }
  // fprintf(stderr, "trace X: <%s>\n", s);
  Lexeme *lex = new_Lexeme(LEX_SYMBOL);
  (*lex).s_value = s;
  return lex;
}

Lexeme* get_lexeme() {
  // fprintf(stderr, "trace F\n");
  while (true) {
    // fprintf(stderr, "trace G\n");
    char c[2];
    c[1] = '\0';
    c[0] = get_char();
    // fprintf(stderr, "trace H: char = <%c>\n", c[0]);
    int rv = regexec(&WHITE_SPACE_RE, c, 0, NULL, 0);
    // fprintf(stderr, "trace h2: rv = %d\n", rv);
    while (! regexec(&WHITE_SPACE_RE, c, 0, NULL, 0)) {
      // fprintf(stderr, "trace I\n");
      c[0] = get_char();
      // fprintf(stderr, "trace J\n");
    }
    // fprintf(stderr, "trace K\n");
    if (! c[0]) {
      // fprintf(stderr, "trace L\n");
      return NULL;  // EOF
    }
    if (c[0] == ';') {
      // fprintf(stderr, "trace M\n");
      read_next_line();
      // fprintf(stderr, "trace N\n");
      continue;
    }
    // fprintf(stderr, "trace O\n");
    if (c[0] == '(') { return new_Lexeme(LEX_LEFT_PAREN); }
    if (c[0] == ')') { return new_Lexeme(LEX_RIGHT_PAREN); }
    if (c[0] == '\'') { return new_Lexeme(LEX_QUOTE); }
    if (c[0] == '"') { return scan_string(); }
    // fprintf(stderr, "trace P\n");
    un_get_char(c[0]);
    // fprintf(stderr, "trace R: <%c>\n", c[0]);
    return scan_word();
  }
}

void main(char **argv) {
  fprintf(stderr, "a\f\n\r\t\v\n");
  // fprintf(stderr, "trace 0\n");
  init_regex();
  // fprintf(stderr, "trace A\n");
  Lexeme *lex = get_lexeme();
  // fprintf(stderr, "trace B\n");
  while (lex) {
    // fprintf(stderr, "trace C\n");
    print_lexeme(lex);
    // fprintf(stderr, "trace D\n");
    lex = get_lexeme();
    // fprintf(stderr, "trace E\n");
  }
  error("Done!");
}

