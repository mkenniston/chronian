"use strict"

var reader_module = require("./reader")
var util = require("./util")

function main() {
  var reader = new reader_module.Reader()
  var lex = reader.read_lexeme()
  while (lex) {
    console.log(lex)
    lex = reader.read_lexeme()
  }
  
  util.fatal_error("Done!")
}

main()

