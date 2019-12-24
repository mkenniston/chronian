#! /usr/bin/env python

# Quick demonstration program to show how to read and use "short_ids.csv".

import sys

# Get the single command-line argument (the key).
def get_arg():
  if len(sys.argv) != 2:
    print "Usage: ", sys.argv[0], "<string to lookup>"
    exit(1)
  return sys.argv[1]

# Read the whole csv file, and parse it into two hash tables.
def read_csv(path):
  primary_names = {}
  short_ids = {}
  fh = open(path)
  for line in fh:
    if line[0] == '#': continue
    fields = line.rstrip().split(',')
    short_id = fields[1]
    primary_names[short_id] = fields[2]
    for name in fields[1:]:
      short_ids[name] = short_id
  fh.close()
  return primary_names, short_ids

# Print the data for the key.
def main():
  primary_names, short_ids = read_csv('short_ids.csv')
  key = get_arg()
  if key not in short_ids:
    print "Key", key, "not found"
    exit(1)
  short_id = short_ids[key]
  primary_name = primary_names[short_id]
  print "IANA name:", primary_name
  print "short ID: ", short_id

main()

