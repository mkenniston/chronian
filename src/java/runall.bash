#!/usr/bin/env bash
# -*- coding: utf-8 -*-

V0="com/chronian/v0"

rm -f $V0/*.class
javac $V0/*.java
cat ../selftest.ulisp | java $V0/ULisp

