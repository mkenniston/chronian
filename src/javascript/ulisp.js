"use strict"

var reader_module = require("./reader")
var error = reader_module.error
var Reader = reader_module.Reader

function main() {
  var reader = new Reader()
  var lex = reader.read_lexeme()
  while (lex) {
    console.log(lex)
    lex = reader.read_lexeme()
  }
  
  error("Done!")
}

main()

