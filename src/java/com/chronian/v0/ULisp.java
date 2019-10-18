
package com.chronian.v0;

import java.util.Stack;
import java.util.Arrays;
import java.util.Collections;
import java.util.regex.Pattern;
import java.util.Scanner;
import com.chronian.v0.Reader;
import com.chronian.v0.Util;

class ULisp {
  public static void main(String args[]) {
    Reader reader = new Reader();
    Reader.Lexeme lex = reader.get_lexeme();
    while (lex != null) {
      System.out.println(lex);
      lex = reader.get_lexeme();
    }
    Util.error("Done!");
  }
}

