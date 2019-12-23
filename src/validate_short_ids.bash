#!/usr/bin/env bash

# This script does some basic validation of the data in short_ids.csv.
# It won't detect a wrong airport code, but it will find some typos and
# missing, extra, or duplicate entries.

MASTER=short_ids.csv
RAW_IDS=raw_ids.$$
BAD_LENGTHS=bad_lengths.$$
DUPS_REMOVED=dups_removed.$$
TEMP=temp.$$
TZ_LONG_IDS=tz_long_ids.$$
CHR_LONG_IDS=chr_long_ids.$$
TZ_REGIONS=tz_regions.$$
CHR_REGIONS=chr_regions.$$

# extract short codes

grep -v "^#" $MASTER | cut -d',' -f2 | sort > $RAW_IDS
NUM_IDS=`wc -l $RAW_IDS | cut -d' ' -f1`

# make sure the lengths are between 1-4 characters

egrep -v '^[A-Z0-9+-]{1,4}$' $RAW_IDS > $BAD_LENGTHS
NUM_BAD_LENGTHS=`wc -l $BAD_LENGTHS | cut -d' ' -f1`
if [ $NUM_BAD_LENGTHS != "0" ]
then
  cat $BAD_LENGTHS
  echo "FAILED - found short ID(s) with invalid characters or invalid length"
  exit 1
else
  echo "All short IDs have valid format"
  rm $BAD_LENGTHS
fi

# make sure there are no duplicates

sort -u < $RAW_IDS > $DUPS_REMOVED
diff $RAW_IDS $DUPS_REMOVED
if [ $? -ne 0 ]
then
  echo "FAILED - found a duplicate short ID"
  exit 1
else
  echo "No duplicate short IDs found"
  rm $RAW_IDS $DUPS_REMOVED
fi

# make sure there are no mismatched long IDs

grep "^Zone" tzdata*/* | tr '	' ' ' | sed -e 's/  */ /g' | cut -d' ' -f2 | sort -u > $TEMP
grep "^Link" tzdata*/* | tr '	' ' ' | sed -e 's/  */ /g' | cut -d' ' -f3 | sort -u >> $TEMP
sort -u $TEMP > $TZ_LONG_IDS

grep -v "^#" $MASTER | cut -d',' -f3- | tr ',' '\n' | sort > $CHR_LONG_IDS

diff $TZ_LONG_IDS $CHR_LONG_IDS
if [ $? -ne 0 ]
then
  echo "FAILED - found mismatched IANA long ID(s)"
  exit 1
else
  echo "All long IDs match IANA names"
  rm $TEMP $TZ_LONG_IDS $CHR_LONG_IDS
fi

# make sure regions codes match

grep -v "^#" tzdata*/zone.tab | tr '	' ',' | cut -d',' -f1,3 > $TEMP

# Fudge some backzone stuff (does not affect user API, but makes it
# a little bit easier to maintain $MASTER).
cat <<! >>$TEMP
CA,America/Montreal
US,America/Shiprock
AQ,Antarctica/South_Pole
CA,America/Coral_Harbour
GB,Europe/Belfast
MD,Europe/Tiraspol
SJ,Atlantic/Jan_Mayen
US,Pacific/Johnston
VN,Asia/Hanoi
!
sort < $TEMP > $TZ_REGIONS

grep -v "^#" $MASTER | grep -v "^," | cut -d',' -f1,3 | sort > $CHR_REGIONS
diff $TZ_REGIONS $CHR_REGIONS
if [ $? -ne 0 ]
then
  echo "FAILED - found mismatched regions codes"
  exit 1
else
  echo "All region codes match"
  rm $TEMP $TZ_REGIONS $CHR_REGIONS
fi

# finish

echo "$NUM_IDS short IDs validated successfully."
exit 0
