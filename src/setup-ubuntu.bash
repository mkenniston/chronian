#!/usr/bin/env bash
# -*- coding: utf-8 -*-

# Prepare an Ubuntu Linux system to run all the tests in all
# supported languages, by installing all the packages needed.
# You will need to run this with "sudo".

apt-get update
apt-get install mit-scheme  # needed to compile lexical scanners
apt-get install python
apt-get install flake8  # lint for python
apt-get install openjdk-8-jdk  # includes both javac and java
apt-get install nodejs  # javascript interpreter
apt-get install gcc  # plain C (not C++) compiler

echo
echo "=================================="
echo

for CMD in "scheme --version" "python --version" "flake8 --version" "javac -version" "java -version" "nodejs --version" "gcc --version"
do
  $CMD
  if [ $? -eq 0 ]
  then
    echo "OK"
  else
    echo "**** FAILED ****"
  fi
done
