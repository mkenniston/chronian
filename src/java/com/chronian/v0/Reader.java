
package com.chronian.v0;

import java.util.Stack;
import java.util.Arrays;
import java.util.Collections;
import java.util.regex.Pattern;
import java.util.Scanner;
import com.chronian.v0.Util;


class Lexeme {
  static final String LEX_INT = "int";
  static final String LEX_FLOAT = "float";
  static final String LEX_STRING = "string";
  static final String LEX_BOOLEAN = "boolean";
  static final String LEX_SYMBOL = "symbol";
  static final String LEX_LEFT_PAREN = "left_paren";
  static final String LEX_RIGHT_PAREN = "right_paren";
  static final String LEX_QUOTE = "quote";

  String type;
  public Lexeme(String type) { this.type = type; }
  protected String format(String value) {
    String result = "<Lexeme, type: " + type;
    if (value != null) {
      result = result + ", value = " + value;
    }
    result = result + ">";
    return result;
  }
}

class IntLexeme extends Lexeme {
  int value;
  public IntLexeme(int n) { super(LEX_INT); this.value = n; }
  public String toString() { return super.format("" + this.value); }
}

class FloatLexeme extends Lexeme {
  float value;
  public FloatLexeme(float f) { super(LEX_FLOAT); this.value = f; }
  public String toString() { return super.format("" + this.value); }
}

class StringLexeme extends Lexeme {
  String value;
  public StringLexeme(String s) { super(LEX_STRING); this.value = s; }
  public String toString() { return super.format("" + this.value); }
}

class BooleanLexeme extends Lexeme {
  boolean value;
  public BooleanLexeme(boolean b) { super(LEX_BOOLEAN); this.value = b; }
  public String toString() { return super.format("" + this.value); }
}

class SymbolLexeme extends Lexeme {
  String value;
  public SymbolLexeme(String s) { super(LEX_SYMBOL); this.value = s; }
  public String toString() { return super.format("" + this.value); }
}

class LeftParenLexeme extends Lexeme {
  public LeftParenLexeme() { super(LEX_LEFT_PAREN); }
  public String toString() { return super.format(null); }
}

class RightParenLexeme extends Lexeme {
  public RightParenLexeme() { super(LEX_RIGHT_PAREN); }
  public String toString() { return super.format(null); }
}

class QuoteLexeme extends Lexeme {
  public QuoteLexeme() { super(LEX_QUOTE); }
  public String toString() { return super.format(null); }
}


class Reader {

  static final Pattern WHITE_SPACE_RE = Pattern.compile("^[ \\f\\n\\r\\t\\u000B]$");
  static final Pattern INTEGER_RE = Pattern.compile("^[+-]?\\d+$");
  static final Pattern FLOAT_RE = Pattern.compile("[+-]?(\\d+[.]?\\d*|[.]\\d+)(e[+-]\\d+)?$");
  static final Pattern BREAK_RE = Pattern.compile("^[ \\r\\n\\r\\t\\u000B()';]$");

  Stack<String> line_buffer = new Stack<String>();
  Scanner input_scanner = new Scanner(System.in);

  void read_next_line() {
    if (input_scanner.hasNextLine()) {
      line_buffer = new Stack<String>();
      String line = input_scanner.nextLine();
      if (line.length() > 0) {
        line_buffer.addAll(Arrays.asList(line.split("")));
      }
      line_buffer.push("\n");
      Collections.reverse(line_buffer);
    } else {
      line_buffer = null;
    }
  }

  String get_char() {
    if (line_buffer != null && line_buffer.isEmpty()) {
      read_next_line();
    }
    if (line_buffer == null) {
      return "";  // end of file
    }
    return line_buffer.pop();
  }

  void un_get_char(String c) {
    line_buffer.push(c);
  }

  static String parse_escaped_string_char(String c) {
    String result = "";
    if (c.equals("")) {
      Util.error("found EOF while reading a string");
    } else if (c.equals("\\")) {
      result = "\\";
    } else if (c.equals("\"")) {
      result = "\"";
    } else if (c.equals("b")) {
      result = "\b";
    } else if (c.equals("f")) {
      result = "\f";
    } else if (c.equals("n")) {
      result = "\n";
    } else if (c.equals("r")) {
      result = "\r";
    } else if (c.equals("t")) {
      result = "\t";
    } else if (c.equals("v")) {
      result = "\u000B";
    } else {
      Util.error("unsupported escape sequence in string");
    }
    return result;
  }

  StringLexeme scan_string() {
    Stack<String> s = new Stack<String> ();
    String c = get_char();
    while (! c.equals("\"")) {
      if (c.equals("\\")) {
        c = parse_escaped_string_char(get_char());
      }
      s.push(c);
      c = get_char();
    }
    return new StringLexeme(String.join("", s));
  }

  Lexeme scan_word() {
    Stack<String> s = new Stack<String>();
    String c = get_char();
    while (! BREAK_RE.matcher(c).matches()) {
      s.push(c);
      c = get_char();
    }
    un_get_char(c);
    String word = String.join("", s);
    if (word.equals("#t")) {
      return new BooleanLexeme(true);
    } else if (word.equals("#f")) {
      return new BooleanLexeme(false);
    } else if (INTEGER_RE.matcher(word).matches()) {
      return new IntLexeme(Integer.parseInt(word));
    } else if (FLOAT_RE.matcher(word).matches()) {
      return new FloatLexeme(Float.parseFloat(word));
    } else {
      return new SymbolLexeme(word);
    }
  }

  public Lexeme get_lexeme() {
    while (true) {
      String c = get_char();
      while (WHITE_SPACE_RE.matcher(c).matches()) {
        c = get_char();
      }
      if (c.equals("")) {
        return null;  // EOF
      } else if (c.equals(";")) {
        read_next_line();  // discard comment
      } else if (c.equals("(")) {
        return new LeftParenLexeme();
      } else if (c.equals(")")) {
        return new RightParenLexeme();
      } else if (c.equals("'")) {
        return new QuoteLexeme();
      } else if (c.equals("\"")) {
        return scan_string();
      } else {
        un_get_char(c);
        return scan_word();
      }
    }
  }
}

