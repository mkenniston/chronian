"use strict"

var sexpr = require("./sexpr")
var util = require ("./util")

const LEX_INT = "int"
const LEX_FLOAT = "float"
const LEX_STRING = "string"
const LEX_BOOLEAN = "boolean"
const LEX_SYMBOL = "symbol"
const LEX_LEFT_PAREN = "left_paren"
const LEX_RIGHT_PAREN = "right_paren"
const LEX_QUOTE = "quote"

function Lexeme(type, value) {
  return {'type': type, 'value': value}
}

class Reader {
  constructor() {
    this.WHITE_SPACE_RE = /^[ \f\n\r\t\v]$/
    this.INTEGER_RE = /^[+-]?\d+$/
    this.FLOAT_RE = /[+-]?(\d+[.]?\d*|[.]\\d+)(e[+-]\d+)?$/
    this.BREAK_RE = /^[ \f\n\r\t\v()';]$/

    this.stdinAll = require("fs").readFileSync("/dev/stdin").toString().split("\n")
    this.stdinAll.reverse()
    this.line_buffer = []
  }

  read_next_line() {
    if (this.stdinAll.length) {
      this.line_buffer = this.stdinAll.pop().split("")
      if (this.stdinAll.length) {
        this.line_buffer.push("\n")  // replace char removed by initial split
      }
      this.line_buffer.reverse()
    } else {
      this.line_buffer = []
    }
  }

  read_char() {
    if (! this.line_buffer.length) {
      this.read_next_line()
    }
    if (! this.line_buffer.length) {
      return ""
    }
    return this.line_buffer.pop()
  }

  un_read_char(c) {
    this.line_buffer.push(c)
  }

  scan_string() {
    var s = []
    var c = this.read_char()
    while (c != '"') {
      if (c == "\\") {
        c = this.read_char()
        if (! c) { util.fatal_error("found EOF while reading a string") }
        else if (c == "\\") { s.push("\\") }
        else if (c == '"') { s.push('"') }
        else if (c == "b") { s.push("\b") }
        else if (c == "f") { s.push("\f") }
        else if (c == "n") { s.push("\n") }
        else if (c == "r") { s.push("\r") }
        else if (c == "t") { s.push("\t") }
        else if (c == "v") { s.push("\v") }
        else { util.fatal_error("unsupported escape sequence in string") }
      } else {
        s.push(c)
      }
      c = this.read_char()
    }
    return Lexeme(LEX_STRING, s.join(""))
  }

  scan_word() {
    var s = []
    var c = this.read_char()
    while (! this.BREAK_RE.test(c)) {
      s.push(c)
      c = this.read_char(c)
    }
    this.un_read_char(c)
    s = s.join("")
    if (s == "#t") { return Lexeme(LEX_BOOLEAN, true) }
    else if (s == "#f") { return Lexeme(LEX_BOOLEAN, false) }
    else if (this.INTEGER_RE.test(s)) { return Lexeme(LEX_INT, parseInt(s)) }
    else if (this.FLOAT_RE.test(s)) { return Lexeme(LEX_FLOAT, parseFloat(s)) }
    else { return Lexeme(LEX_SYMBOL, s) }
  }

  read_lexeme() {
    while (true) {
      var c = this.read_char()
      while (this.WHITE_SPACE_RE.test(c)) {
        c = this.read_char()
      }
      if (! c) {
        return null
      } else if (c == ";") {
        this.read_next_line()
        continue
      } else if (c == "(") {
        return Lexeme(LEX_LEFT_PAREN, null)
      } else if (c == ")") {
        return Lexeme(LEX_RIGHT_PAREN, null)
      } else if (c == "'") {
        return Lexeme(LEX_QUOTE, null)
      } else if (c == '"') { return this.scan_string() }
      else {
        this.un_read_char(c)
        return this.scan_word()
      }
    }
  }
}

exports.Reader = Reader

