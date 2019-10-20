"use strict"

var reader_module = require("./reader")
var fatal_error = reader_module.fatal_error
var Reader = reader_module.Reader

function main() {
  var reader = new Reader()
  var lex = reader.read_lexeme()
  while (lex) {
    console.log(lex)
    lex = reader.read_lexeme()
  }
  
  fatal_error("Done!")
}

main()

