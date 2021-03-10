"use strict"

class SExpr {
  constructor() {
  }

  to_string(self) {
    return "<SExpr of unknown type>"
  }
}

class List extends SExpr {
  constructor(left, right) {
    this.left = left
    this.right = right
  }

  to_string(self) {
    rest = this
    var result = []
    while (rest) {
      result.push(rest.left.to_string())
      rest = rest.right
    }
    result.push(")")
    return " ".join(result)
  }
}

exports.SExpr = SExpr
exports.List = List

