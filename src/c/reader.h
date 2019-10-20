#ifndef READER_H
#define READER_H

#include <stdbool.h>

typedef struct {
  const char* type;
  union {
    char* s_value;
    int i_value;
    float f_value;
    bool b_value;
  };
} Lexeme;

typedef struct {
  char* line_buffer;
  char* cur_char;
} Reader;

void error(char *msg);
void Lexeme_print(Lexeme *pThis);
Reader* Reader_new();
Lexeme* Reader_read_lexeme(Reader *pThis);

#endif  /* READER_H */

