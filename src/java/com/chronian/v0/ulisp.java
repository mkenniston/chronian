
package com.chronian.v0;

import java.util.Stack;
import java.util.Arrays;
import java.util.Collections;
import java.util.regex.Pattern;
import java.util.Scanner;
import com.chronian.v0.Lexeme;
import com.chronian.v0.Reader;
import com.chronian.v0.Util;

class ULisp {
  public static void main(String args[]) {
    Reader reader = new Reader();
    Lexeme lex = reader.read_lexeme();
    while (lex != null) {
      System.out.println(lex);
      lex = reader.read_lexeme();
    }
    System.out.println("Done!");
  }
}

