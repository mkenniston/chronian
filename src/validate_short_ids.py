#! /usr/bin/env python

# Do some basic validation of the data in short_ids.csv.
# This won't detect a wrong airport code, but it will find some
# typos and missing, extra, conflicting, or duplicate entries.

import os
import re


def read_csv_file(path):
    primary_names = {}
    short_ids = {}
    regions = {}
    fh = open(path)
    for line in fh:
        if line[0] == '#':
            continue
        fields = line.rstrip().split(',')
        short_id = fields[1]
        if short_id in primary_names:
            print("FAILED -- short ID '%s' is duplicated" % short_id)
            exit(1)
        primary_names[short_id] = fields[2]
        regions[short_id] = fields[0]
        for name in fields[2:]:
            if name in short_ids:
                print("FAILED -- name '%s' is duplicated" % name)
                exit(1)
            short_ids[name] = short_id
    fh.close()
    for id in ['ZULU', 'TAI', 'UT0', 'UT1', 'UT2', 'TT', 'GPS']:
        if id in primary_names:
            print("FAILED -- short ID '%s' is reserved" % id)
            exit(1)
    print("No duplicate short IDs or long names found")
    return primary_names, short_ids, regions


def validate_short_id_format(primary_names):
    p = re.compile('^[A-Z0-9+-]{1,4}$')
    for id in primary_names.keys():
        if not p.match(id):
            print("FAILED -- short ID '%s' has invalid format or length" % id)
            exit(1)

    print("All short IDs have valid format")


def read_tz_long_names():
    long_names = {}
    zpat = re.compile("^Zone")
    lpat = re.compile("^Link")
    for line in os.popen("cat tzdata*/*").read().split('\n'):
        if zpat.match(line):
            long_names[line.split()[1]] = True
        elif lpat.match(line):
            long_names[line.split()[2]] = True
    return long_names


def validate_long_names_match(short_ids):
    tz = read_tz_long_names()
    for name in tz:
        if name not in short_ids.keys():
            print("FAILED -- tzdata name '%s' not found" % name)
            exit(1)
    for name in short_ids.keys():
        if name not in tz:
            print("FAILED -- name '%s' not found in tzdata" % name)
            exit(1)
    print("All long IDs match tzdata names")


def validate_region_codes_match(primary_names, short_ids, regions):
    # Read regions defined in tzdata.
    tz_regions = {}
    comment_pat = re.compile('^#')
    for line in os.popen("cat tzdata*/zone.tab").read().split('\n'):
        if comment_pat.match(line) or len(line.rstrip()) == 0:
            continue
        fields = line.split()
        tz_regions[fields[2]] = fields[0]

    # Fudge some backzone stuff (does not affect user API, but makes it
    # a little bit easier to maintain short_ids.csv file).
    for region, long_name in [
            ['AQ', 'Antarctica/South_Pole'],
            ['CA', 'America/Coral_Harbour'],
            ['CA', 'America/Montreal'],
            ['GB', 'Europe/Belfast'],
            ['MD', 'Europe/Tiraspol'],
            ['SJ', 'Atlantic/Jan_Mayen'],
            ['US', 'Pacific/Johnston'],
            ['US', 'America/Shiprock'],
            ['VN', 'Asia/Hanoi'],
            ]:
        tz_regions[long_name] = region

    # Compare our regions with tzdata.
    for long_name in short_ids.keys():
        our_reg = regions[short_ids[long_name]]
        if long_name not in tz_regions:
            continue
        tz_reg = tz_regions[long_name]
        if our_reg != tz_reg:
            print("FAILED -- '%s' has region '%s' but tzdata has '%s'" %
                  (long_name, our_reg, tz_reg))
            exit(1)
    print("All region codes match tzdata")


def validate_2char_ids_match_regions(regions):
    for id in regions.keys():
        if len(id) != 2:
            continue
        if id != regions[id]:
            print("FAILED -- short ID '%s' does not match region '%s'" %
                  (id, regions[id]))
            exit(1)
    print("All 2-char short IDs match their own region code")


def validate_short_matches_long(primary_names, short_ids):
    for name in short_ids.keys():  # look at every long name
        if name in primary_names.keys():  # is it also a short name?
            if name != short_ids[name]:  # does it match?
                print("FAILED -- name '%s' has short ID '%s'" %
                      (name, short_ids[name]))
    print("No short IDs conflict with long names")


def main():
    primary_names, short_ids, regions = read_csv_file("short_ids.csv")
    validate_short_id_format(primary_names)
    validate_long_names_match(short_ids)
    validate_region_codes_match(primary_names, short_ids, regions)
    validate_2char_ids_match_regions(regions)
    validate_short_matches_long(primary_names, short_ids)
    print("%d entries validated successfully" % (len(primary_names)))
    exit(0)

main()
