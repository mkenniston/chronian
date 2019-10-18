
const LEX_INT = "int"
const LEX_FLOAT = "float"
const LEX_STRING = "string"
const LEX_BOOLEAN = "boolean"
const LEX_SYMBOL = "symbol"
const LEX_LEFT_PAREN = "left_paren"
const LEX_RIGHT_PAREN = "right_paren"
const LEX_QUOTE = "quote"

const WHITE_SPACE_RE = /^[ \f\n\r\t\v]$/
const INTEGER_RE = /^[+-]?\d+$/
const FLOAT_RE = /[+-]?(\d+[.]?\d*|[.]\\d+)(e[+-]\d+)?$/
const BREAK_RE = /^[ \f\n\r\t\v()';]$/

var stdinAll = require("fs").readFileSync("/dev/stdin").toString().split("\n")
stdinAll.reverse()
var line_buffer = []

function Lexeme(type, value) {
  return {'type': type, 'value': value}
}

function error(msg) {
  console.log(msg)
  process.exit(1)
}

function read_next_line() {
  if (stdinAll.length) {
    line_buffer = stdinAll.pop().split("")
    if (stdinAll.length) {
      line_buffer.push("\n")  // replace char removed by initial split
    }
    line_buffer.reverse()
  } else {
    line_buffer = []
  }
}

function read_char() {
  if (! line_buffer.length) {
    read_next_line()
  }
  if (! line_buffer.length) {
    return ""
  }
  return line_buffer.pop()
}

function un_read_char(c) {
  line_buffer.push(c)
}

function scan_string() {
  var s = []
  var c = read_char()
  while (c != '"') {
    if (c == "\\") {
      c = read_char()
      if (! c) { error("found EOF while reading a string") }
      else if (c == "\\") { s.push("\\") }
      else if (c == '"') { s.push('"') }
      else if (c == "b") { s.push("\b") }
      else if (c == "f") { s.push("\f") }
      else if (c == "n") { s.push("\n") }
      else if (c == "r") { s.push("\r") }
      else if (c == "t") { s.push("\t") }
      else if (c == "v") { s.push("\v") }
      else { error("unsupported escape sequence in string") }
    } else {
      s.push(c)
    }
    c = read_char()
  }
  return Lexeme(LEX_STRING, s.join(""))
}

function scan_word() {
  var s = []
  var c = read_char()
  while (! BREAK_RE.test(c)) {
    s.push(c)
    c = read_char(c)
  }
  un_read_char(c)
  s = s.join("")
  if (s == "#t") { return Lexeme(LEX_BOOLEAN, true) }
  else if (s == "#f") { return Lexeme(LEX_BOOLEAN, false) }
  else if (INTEGER_RE.test(s)) { return Lexeme(LEX_INT, parseInt(s)) }
  else if (FLOAT_RE.test(s)) { return Lexeme(LEX_FLOAT, parseFloat(s)) }
  else { return Lexeme(LEX_SYMBOL, s) }
}

function read_lexeme() {
  while (true) {
    var c = read_char()
    while (WHITE_SPACE_RE.test(c)) {
      c = read_char()
    }
    if (! c) { return null }
    else if (c == ";") {
      read_next_line()
      continue
    } else if (c == "(") { return Lexeme(LEX_LEFT_PAREN, null) }
    else if (c == ")") { return Lexeme(LEX_RIGHT_PAREN, null) }
    else if (c == "'") { return Lexeme(LEX_QUOTE, null) }
    else if (c == '"') { return scan_string() }
    else {
      un_read_char(c)
      return scan_word()
    }
  }
}

var lex = read_lexeme()
while (lex) {
  console.log(lex)
  lex = read_lexeme()
}

error("Done!")

