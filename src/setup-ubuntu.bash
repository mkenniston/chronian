#!/usr/bin/env bash
# -*- coding: utf-8 -*-

# Prepare an Ubuntu Linux system to run all the tests in all
# supported languages, by installing all the packages needed.
# You will need to run this with "sudo".

apt-get install python
apt-get install javacc
apt-get install java-sdk
apt-get install node
apt-get install gcc
apt-get install flake8

