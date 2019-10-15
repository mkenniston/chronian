#!/usr/bin/env bash
# -*- coding: utf-8 -*-

echo "=== PYTHON ==="
(cd python; ./runall.bash; cd ..)

echo "=== JAVA ==="
(cd java; ./runall.bash; cd ..)

echo "=== JAVASCRIPT ==="
(cd javascript; ./runall.bash; cd ..)

echo "=== C ==="
(cd c; ./runall.bash; cd ..)

