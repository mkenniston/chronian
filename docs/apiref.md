[back to Table of Contents](TOC.md)

# Chronian -- API Reference

This document describes each class, constant, and method in **chronian**.

## class Chron

### Constants

```
# constants for day_of_week

chron.MON, chron.MONDAY
chron.TUE, chron.TUESDAY
chron.WED, chron.WEDNESDAY
chron.THU, chron.THURSDAY
chron.FRI, chron.FRIDAY
chron.SAT, chron.SATURDAY
chron.SUN, chron.SUNDAY

# constants for month

chron.JAN, chron.JANUARY
chron.FEB, chron.FEBRUARY
chron.MAR, chron.MARCH
chron.APR, chron.APRIL
chron.MAY
chron.JUN, chron.JUNE
chron.JUL, chron.JULY
chron.AUG, chron.AUGUST
chron.SEP, chron.SEPTEMBER
chron.OCT, chron.OCTOBER
chron.NOV, chron.NOVEMBER
chron.DEC, chron.DECEMBER
```

### Constructor

*Chron* is the only class with a public constructor.  Chron objects serve two purposes:
* they serve as a package to hold all the other identifiers
* they allow you to set default parameters for ChronLines

```
chron = Chron()  # create a Chron object with default parameters
chron = Chron(line_spec)  # create a Chron object, overriding defaults with a spec
```

### Methods

```
line = chron.line(line_spec)  # create a ChronLine
spec = chron.line_spec()  # create a ChronLineSpec
```

## class ChronInterval

## class ChronIntervalSpec

## class ChronIntervalSet

## class ChronLine

### Methods

```
```

## class ChronLineSpec

### 

## class ChronPoint

## class ChronPointSpec

---
Copyright (c) 2016 Michael S. Kenniston
