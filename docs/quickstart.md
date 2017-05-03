[back to Table of Contents](TOC.md)

# Chronian -- Quick Start

## Overview 

**chronian** is available in multiple languages.
This QuickStart shows examples in Python, but it should be obvious how to do the same things in other languages.
For more details, see the API Reference.

This QuickStart is only intended to show you how to get started, so it describes only the most basic features.
Refer to the API Reference to see the full range of options and capabilities available in **chronian**.

There are four primary classes in **chronian** that you need to know about:
* **Chronian** - This is a container for all the configuration options you choose, and it is also the root of the namespace.
You will typically create a single Chronian object called "chron" and use it everywhere in your program.
* **ChronLine** - In theory this is a set of related ChronPoints, but in practice it is used much like a timezone.
You will use the "chron" object to create one ChronLine for each timezone you use.
* **ChronPoint** - These are the actual "datetime" objects that represent a specific point in time.
You use ChronLine objects to create ChronPoints.
* **PointSpec** - This is just a data structure which contains all the unpacked fields of a ChronPoint.

Chronian, ChronLine, and ChronPoint objects are all immutable, which makes them thread-safe without requiring any special locking mechanism.

PointSpecs are mutable, since they are intended as temporary "scratchpads" where you can stuff data while you are manipulating it.
They should generally be used only as thread-local variables.

All of Chronian is based on factories, so you will not be calling any constructors explicitly.

## Getting Started

You need to get access to the name "Chronian" in whatever manner is appropriate for the language you are using, e.g. "import", "include", "require", etc.

The next thing required in any program is to create a Chronian object.
There are options available, but most people will use the defaults:
```
chron = Chronian.create()
```
You must make the "chron" object available throughout your program; how you do that is completely up to you.
For example, you could:
* use a global variable, or
* use method or contructor parameters to dependency-inject it everywhere it is needed, or
* define a singleton class to create it and provide access to it.

## Defining timezones

Unlike most temporal libraries, in **chronian** timezones are a central object rather than an attribute tagged onto things as an afterthought.
You must create a ChronLine object for each timezone you need, using a factory method of your "chron" object:
```
utc = chron.line("UTC")
pacific_time = chron.line("America/Los_Angeles")
```
Chronian recognizes all the IANA-defined standard names for timezones.

## Creating points

ChronLines are themselves factories for ChronPoints, which are created in a fairly conventional way:
```
my_dob = pacific_time.point(1992, 10, 14)
utc_effective_at = utc.point(2017, 6, 15, 12, 0, 0)
```

## Timezone conversion

ChronPoints are immutable, so any conversions or other manipulations are done by creating new ChronPoint objects:
```
local_effective_at = pacific_time.point(utc_effective_at)
```

## Checking if two points are the same

There are three types of "sameness" you can check for.
It is your responsibility as the application programmer to decide which type you need:
* Object identity - this means two ChronPoints are the same object, i.e. have the same address in memory.
Use your language's standard way of checking this:
```
if point1 is point2:
```
* Value equality - this means two ChronPoints may be distinct objects in memory, but are otherwise indistinguishable.
If your language has a standard way of checking this use it, otherwise use the "equals" method:
```
if point1 == point2:
```
* Simultaneity - this means that two ChronPoints represent the same instant in time, even though it may be expressed differently (e.g. in different timezones).
Use the "is_simultaneous" method:
```
if point1.is_simultaneous(point2)
```

## Determining the order of points

**chronian** defines two types of ordering.
It is your responsibility as the application programmer to decide which type you need:
* Temporal ordering - this determines which ChronPoint came first, regardless of what timezone they might be in:
```
if point1.is_before(point2):
if point1.is_after(point2):
if point1.is_before_or_simultaneous(point2)
if point1.is_after_or_simultaneous(point2)
if point1.is_simultaneous(point2)
if point1.is_not_simultaneous(point2)
```
* Sort ordering - this defines a somewhat arbitrary total ordering on all ChronPoints of all timezones (based on value, not object-address).
This is intended for use in binary search, balanced trees, etc.
```
comp = point1.compare(point2)  # returns -1, 0, or +1
```
Sorting a list by sort-order will *not* necessarily place the items in temporal order.

## Input: Parsing points

You can create a point from a string in the conventional way:
```
point = line.point(input_string, format_string)
```

If the string has a parseable timezone in it, **chronian** can create the ChronLine for you:
```
point = chron.point(input_string, format_string)
```

## Output: formatting points

You can generate a string representation of a point using your language's conventional method (e.g. to_s(), to_string(), etc.), or the to_string method if the langauge has no convention.
```
print str(point)  # default formatting
print point.to_string(format_string)  # user-specified formatting
```

## Reading fields of a point

Each ChronPoint is stored in an opaque, compact, internal format.
Before you can read the individual fields, you must convert it to a PointSpec:
```
spec = point.spec()
print spec.year(), spec.month(), spec.day_of_month(), spec.day_of_week()
print spec.hour(), spec.minute(), spec.second(), spec.fraction()
print spec.tz_name()
```

## Writing fields of a point

Since ChronPoints are immutable you cannot change a ChronPoint's field values.
However, you can convert a point to a spec, change fields of the spec, then create a new point:
```
spec = point1.spec()
spec.year(2014)
spec.hour(17)
point2 = pacific.point(spec)
```

For convenience the setter methods are chainable, so more concisely:
```
point2 = pacific.point(point1.spec().year(2014).hour(17))
```

## Performing arithmetic on points

Don't.

Really, don't do it.  Ever.  Friends don't let friends do temporal arithmetic.

Just say no.

Date/time/timezone logic is so convoluted and irregular and filled with bizarre edge cases that you are very unlikely to get it right.
Handling all that nastiness is the job of the library -- in this case **chronian**, but the point applies to any temporal library.
The authors of such libraries put more time and effort into it than you can afford to spend, so leverage their investment.

The catch is that some arithmetic appears so trivial that you don't even notice that you're doing arithmetic at all.
If you ever find yourself applying "<", ">", "+", "-", or any of their related operators to date/time related values, **STOP**.
Think about what you are really trying to do, and find a way to ask the library to do it for you.
In the worst case the library may not have a way to do it, in which case you either extend the library (with lots of new unit tests) or get a new library.
Do NOT put temporal logic in your application code, no matter how innocuous it might seem.

## Asking the library to perform arithmetic on points

Of course there will be times when arithmetic manipulation of ChronPoints is needed, so **chronian** provides methods for that:
```
point2 = point1.plus(days=5)  # exactly 5 days later
point2 = point1.beginning_of_day()
point2 = point1.minus(months=1)  # same day last month
```

See the full API reference for a list of everything available.

## Still feeling tempted by the forbidden?

OK, let's go step on a few landmines and see how it feels.

Given a ChronPoint, find the same time the next day.
That sounds straightforward:
```
spec = point1.spec()
spec.day_of_month(spec.day_of_month() + 1)
point2 = line.point(spec)
```
Test it for May 29, the result is June 29.

Test it for May 30, the result is June 30.

Test it for May 31, the result is June 31.

_Oops, there is no June 31._

No problem, we'll add an array of month-lengths and check for wrap-around:
```
MONTH_LENGTH = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
while spec.day_of_month() > MONTH_LENGTH[spec.month() - 1]:
    spec.month((spec.month % 12) + 1)
    spec.day_of_month(spec.day_of_month() - MONTH_LENGTH[spec.month() + 1]
```
Well, that's a big ugly, but it should work.

Test it for Jan 31, the result is Feb 1.

Test it for Feb 28, the result is Mar 1.

_Oops, or should that be Feb 29?  It depends on the year._

Right, we just need a leap-year check for divisible-by-4, and don't forget the special divisible-by-100 rule:
```
def month_length(y, m):
    leap = (y % 4 == 0) and (y % 100 != 0)
    if m == 2 and leap:
        return 29
    return MONTH_LENGTH[m]
```

Good, now test it for Feb 2000.

_Oops, 2000 was really a leap year._

Well, it was almost right, just add the special rule for divisible-by-400.
```
... and ((y % 100 != 0) or (y % 400 == 0))
```
Now test for Dec 31, the result is Jan 1.

_Oops, the year didn't increment._

Rats, add more code to handle year wrap-around.
```
   if spec.month() == 1:
       spec.year(spec.year() + 1)
```
Now test for 2017-03-11 02:30:00, the result is 2017-03-12 02:30:00

_Oops, there was no 2:30 AM on March 12, since that's when Daylight time started.

```
# add more code to handle DST changes
```
Now test it for 2016-12-31 23:59:60, the result is 2017-01-01 23:59:60.

_Oops, that was a leap second which only appeared for one day.
```
# add even more code to handle leap seconds
```

Now test it for 1752-09-02, the result is 1752-09-03.

_Oops, the next day was actually 1752-09-14 (at least in England and the colonies), since that's when the calendar switched from Julian to Gregorian.
```
# add EVEN MORE code to handle calendar switches
```
And by the way, there is at least one bug in the code snippets above.
You did catch it, didn't you?

Let's stop here for a moment and ask:  What does any of this have to do with building my amazing new app that scrapes Twitter and Uber data to find the most popular entertainent venues?

The answer, of course, is Absolutely Nothing.
Implementing date/time details like that is simply wasting your time to write an incorrect version of code that somebody else already wrote and tested.
Now ponder this for a moment: all that trouble was just for "d = d + 1".
Imagine what it would be like for anything more complex.

_Never do temporal arithmetic in application code._

---
Copyright (c) 2017 Michael S. Kenniston.
