"use strict"

function fatal_error(msg) {
  console.log(msg)
  process.exit(1)
}

exports.fatal_error = fatal_error
