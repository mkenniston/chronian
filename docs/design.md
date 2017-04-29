[back to Table of Contents](TOC.md)

# Chronian -- Design Philosophy

Nothing in this section is required to understand how **chronian** works or to use it effectively.  The material here explains the *why* behind how the library works.

## Cross-Language Implementation

This is one of the two major reasons that the **chronian** library exists.  Like many experienced programmers, as I moved from project to project over the course of many years, it was constantly necessary to learn and use new languages.  That was OK because each new language generally had something new or different which made it attractive and useful.  The best languages even help you to develop new ways of thinking so your mind doesn't get old and moldy.

However, what was not OK was having to learn a gratuitously different API and semantics for date-and-time computation every time I switched languages.  After all, we don't need to learn a whole new form of SQL or Regular Expressions for each application language, so why should we waste precious brain cells learning new date-and-time APIs?  I got really tired of that, and there was always plenty of useful work needing to be done which could make better use of my finite mental capacity.

One interesting twist to this design goal is that **chronian** identifiers must not conflict with any reserved word in *any* supported language.  This requires some foresight, so the list of prohibited names was initially constructed from the "reserved words" lists of every language that might someday be a porting target.

## Using the Chronian Model

This is the other main reason the library was created.  Even with the best of existing libraries, things always seemed to me to be more complex than they need to be.  After years of on-and-off tinkering and pondering (going way back to 1997 with Y2K work), I finally stumbled onto the idea of modeling temporal computation using multiple ChronLines.  Things really did get easier (note I said *easier*, not *easy*) to understand once I started thinking in those terms, and once a few good libraries were available as a foundation it became feasible to do a prototype implementation of a **chronian** API without spending years of spare time to get it working.  What you see here is the result of that: an experiment to see if the Chronian model works in practice.

## Immutable Date-Time objects

The Joda-Time library makes its objects immutable, and the rationale for it is so compelling that I adopted it for **chronian** as well.  The most powerful reason is to make all such objects thread-safe without the need for any special synchronization code or overhead, but I also find it easier to reason about temporal code when you don't have to remember whether an object has had any fields changed.

## Use of Factory Methods

By convention **chronian** hides most raw constructors for date-time objects, instead providing factory methods to create them.  While this practice is not essential to the conceptual framework, it has a number of advantages:
* it is convenient and concise
* it improves cross-language syntax consistency
* it leaves a lot of latitude when doing language-ports to use whatever namespacing and/or class-nesting techniques are customary and appropriate for each target language
* it encourages good practice (injection and mocking) in automated tests.

## Static vs. Dynamic Type-Checking

This is an interesting question for software that is intended to be ported to many languages with radically different ideas about it, for example Python/Ruby vs. Java/C++.  The way **chronian** handles this is to design the syntax and semantics so that static type-checking will work smoothly when needed, but terse source code will still be natural in languages that encourage that.  Hiding constructors and enabling call-chaining helps a lot here, since the actual types often need not be explicitly mentioned.

Either way, we run the same unit tests on everything in all supported languages, so the whole testing argument really doesn't apply here.

## Concise vs. Explicit

A designer often has to make a choice between a notation that is concise and a notation that is very explicit.  Of course programmers prefer to write code that is short, but code is read more often than it is written.  Here things get a bit murkier, because all other things being equal short code is also easier to read -- but all other things are usually not equal.

The guideline I've used in **chronian** is to keep things sufficiently explict that (1) strict compile-time checking is possible, and (2) the reader can tell what is happening with minimal knowledge of "special magic", even if an operation is not explicitly called out.  One main place this question arose is in the implicit creation of Spec objects; here I judged the magic to be minimal because:
* there is a simple rule "calling a setter method always returns a spec object"
* this rule can be clearly referenced and easily found in each setter's documentation
* the gain in reduced code clutter makes **chronian** more competitive with existing libraries
* the programmer still has the option of writing out the explict creation

## Spec Objects

Although the core objects are immutable, there are times when you just want a plain old struct with mutable fields.  Spec objects fill this role in **chronian**.  By default they are not thread-safe, and so should be used as local scratch areas within a  thread, but they can be frozen to make them immutable.  Note that Spec objects are meant as a way to specify how you want to construct or format date-time objects, not as a way to store them, and *never* as a way to compute with them.  Because of that, values in Spec objects are never validated -- you can put anything you want into them, and they will only be checked if/when you use them to create a base object.

Spec objects have their roots in Joda-Time's "Partials", but **chronian** extends their application to uses somewhat like regular expressions.

There are three classes of Spec objects, each with allowed Fields.  It is critical that the field names are disjoint, so you can infer the type from the field name alone:

* LineSpec
    * date_system
    * time_system
    * leap_seconds
    * resolution
    * time_zone_id

* PointSpec
    * year
    * month
    * day_of_month
    * hour
    * minute
    * second
    * fraction
    * day_of_week

* DurationSpec
    * years
    * months
    * weeks
    * days
    * hours
    * minutes
    * seconds
    * fractions

For consistency, all three Spec classes work the same way.  Each class XXX (ChronLine, ChronPoint, or Duration) has the following factory methods for creating XXXSpec objects:

```
# creating an empty spec
some_spec = chron.point_spec()
some_spec = chron.line_spec()
some_spec = chron.duration_spec()

# creating a populated spec
some_spec = chron.point_spec(arg, ...)
some_spec = chron.line_spec(arg, ...)
some_spec = chron.duration_spec(arg, ...)

# creating a spec populated with values from an existing object
some_spec = some_point.spec()
some_spec = some_line.spec()
some_spec = some_duration.spec()

# creating a new copy of a spec
some_spec = other_spec.clone()

# creating an empty spec, then changing a field value
some_point = chron.year(val)
some_line = chron.resolution(val)
some_duration = chron.years(val)

# creating a populated spec, then changing a value
some_spec = some_point.month(val)
some_spec = some_line.resolution(val)
some_spec = some_duration.months(val)

# creating an immutable (and thus thread-safe) copy of a spec
some_spec = other_spec.frozen()
```

You can access and change the fields of a spec with these methods:

```
val = some_spec.field()            # returns the value of field
same_spec = some_spec.field(val)   # changes the value of a field (mutator) and returns the spec
```

The two methods that create a Spec object and change one field value in a
single step are convenience methods and could be omitted, e.g. "obj = chron.month(chron.JAN)" does exactly the same thing as "obj = chron.point_spec().month(chron.JAN)".  See the discussion of "concise vs. explicit" for details of why both are included.

## "Fluent" and Chained Method Calls

Important parts of **chronian** require the ability to specify some arguments and leave others undefined.  Keyword arguments are a clean way to implement that, but many of the languages targeted by **chronian** don't support keyword arguments.  Using chained method calls was the clearest, most concise way that I could find to serve this purpose while still having similar syntax across most languages.

Here are some examples:

```
# Create a new spec.
point_spec = chron.year(2001).month(9).day_of_month(11)

# Find when 4th of July starts/started this year.
independence = (clock.read(pacific)
                     .month(7).day_of_month(4)
                     .to(pacific)
                     .start_of_day())

# Same thing, another way:
independence = pacific.point(clock.read(pacific).year(), 7, 4)
```

## Naming Conventions and Conversions

Choose names that are (1) clear, and (2) short.

Although the Chronian model uses the terms ChronLine and ChronPoint, identifiers within the **chronian** library shorten those to "line" and "point".

Converting a TypeA object to a TypeB object using instance methods:

```
b_instance = a_instance.to_type_b(args, ...)  # for any compatible TypeB
b_instance = a_instance.to(args, ...)         # for the most common conversion
```

Creating a TypeB object from a TypeA object using factory methods:

```
b_instance = parent_of_b_instance.type_b_from_type_a(a_instance)
# e.g. pacific_point = pacific_line.point_from_point(any_point)
b_instance = parent_of_b_instance.type_b(a_instance)
# for most common conversion, and also when the language supports multiple method signatures
#e.g. pacific_point = pacific_line.point(any_point)
```

In most cases the "to" methods simply call the "from" factory methods, but both are provided for convenience and to increase code clarity.  N.B.:  the method name is always "a_from_b" or "a".  It is never a bare "from" because "from" is a reserved word in Python.

## Leap Seconds Support

Leap seconds are inconvenient, but they're real.  Deal with it, and write code that gives right answers.  It drives me crazy to use a library which cannot do a simple UTC calculation correctly.  (Both Unix/Linux and Windows do this wrong -- even the very definition of time_t is wrong, i.e. it claims to be "seconds past UTC epoch" but is actually "non-leap seconds past UTC epoch".)

On the other hand, the habit of ignoring leap seconds is embedded in a zillion systems and ingrained in a zillion programmers, so for compatibility **chronian** reluctantly makes "ignore leap seconds" the default.  Ignoring leap seconds also makes the initial prototype *much* easier to build -- but the architecture is there to support leap seconds seamlessly later.

## Simple synax and semantics

No library with clumsy syntax is going to attract many users, so it's a given that everything must be structured in a way that is at least as easy to use as more traditional temporal libraries.  Ideally, **chronian** structure will also illuminate the semantics of the underlying model, and that's what I was striving for in this design.

## Opaque Classes

This seems like a no-brainer, but far too many existing temporal libraries (not all, but many) are implemented using abstractions so leaky that you cannot predict the result of a function call without understanding details of the representation.  This is simply not acceptable, so you will find that the documentation for **chronian** deliberately avoids telling you what the underlying representation is.  For any other type of class this would just be common best practice, and it should be for temporal classes as well.

## Clocks Distinct from Date-Times

Most existing temporal libraries have something like "MyLib.now()" to read the current time.  No, no, no!  A clock is not a data type or a data object, it's an interface to a piece of hardware that *returns* a data object.  Furthermore, if you make it easy to inject or mock a clock for your automated unit tests, your life will get ever so much easier -- and your code will more clearly state what it's actually doing.  Clocks in **chronian** remain distinct from all the data types, although they are *aware* of the data types.

This is also one specific case of **chronian** eschewing class methods.

## Compact (4-char) Time Zone Ids

I struggled with this one.  The basic problem is that in order for a time-point to be properly serialized for persistence, it has to include a time zone.  The IANA time zone names are widely accepted as *the* standard so we have to be compatible with that -- but the official names are so long that most programmers just couldn't stomach storing such a large string with every single time point.  In addition, I personally couldn't stomach making up a special, incompatible set of codes just for my own library (and still don't understand why RoR did exactly that).  After a bit of searching, I found a compromise by using another widely-accepted international standard: the airport codes assigned by IATA (or in a few cases, ICAO).  Since most time zones are named after a large city (or a whole country), there is an airport associated with nearly every one, and people in the area are already familiar with the codes.  No literate US resident would find it difficult to guess where LAX, DEN, CHI, and NYC are, and nobody in France or the U.K. would have any trouble deciphering LON or PAR.

The ICAO list is more inclusive so it would seem simpler to just use that for all the codes, but we prefer the IATA code when there is one because (1) The IATA codes are shorter, and (2) the IATA codes are better known (they are the ones on your luggage tags).

Of course the actual translation is all just table look-up, but if you're curious the algorithm for assigning these codes is:

0. When a number of IANA names are synonyms for semantically equivalent time zones, they can all map to the same short code.  For example, "UTC", "GMT", "GMT+0", "Zulu", and "Etc/Zulu" all mean the same thing, so they can all map to "Z".
However, just being linked does not make two zones equivalent, e.g. even when a country currently uses one zone it still reserves the right to change in the future, so we count (and code) that country's zone as distinct.
1. If the zone is defined as an offset, code it as "+/-HH" (e.g. "-07").  If the offset is fractional, add "1", "3", or "4" at the end to represent :15, :30, and :45.
2. Extract the name of the city (or region, or country) from the IANA id.  If the name isn't that format, skip ahead.
3. If IATA defines a code for the whole city or metro area, use that (e.g. NYC).
4. Find the largest airport in the city/region, or the nearest airport if the city has none of its own.
5. If IATA defines a 3-letter code for that airport, use it (e.g. LAX).
6. If ICAO defines a 4-letter code for that airport, use it.
7. If you get here, go back to step 4 and choose the next largest airport in the time zone.
8. If there are no coded airports in the time zone, use "*CCC" where CCC is the first 3 consonants of the city/region name.
9. If you have any duplicates, change one of them.

## Multiple Comparison Functions

The three types of equality (pointer equality, value equality, and temporal equality) are distinctly different, so the library should reflect that and allow the application programmer to say *exactly* what kind of comparison is intended.  The first two are generally supported by the language already so there is no need to invent any syntax for that, but temporal comparison needs a notation so we use the methods before (<), before_simultaneous (<=), simultaneous (=), after_simultaneous (>=), and after (>) to make the semantics very clear.

Similarly, we need a stable, predictable way to sort temporal objects.  The sort_compare method meets that need.

## Customizations

One of my pet peeves is that temporal libraries usually force you to use *their* definition of the "right" time line.  If your application requires something slightly different, too bad.  Although I expect that probably over 95% of all **chronian** users will just take the defaults, the Chronian model made it relatively easy to allow customization, thus giving each programmer the tools to get correct answers to *their* problems.

## Allowing Multiple tzinfo Versions

This may seem over-the-top, but there is one specific use case which drives this design decision:  Testing that a program or system functions correctly when run before a tzinfo update and then run again after the update.  **chronian** itself has to have this as part of its automated test suite, but it's entirely reasonable (if perhaps rare) for an application programmer to want the same capability.

A second reason, less compelling but still important, is that automated testing is made easier if we can create special tzinfo files containing weird edge cases that we want to test.

## Namespacing

In large systems namespace pollution can be serious, so **chronian** limits itself to insering *one* name into your namespace.  Everything else is derived off of that.  If you need something guaranteed globally unique, I registered "chronian.com" in part so you can use com.Chronian as the name.

Although not required by the model, for simplicity **chronian** uses the convention that classes have only instance methods, never class methods.  This is easy to remember, and it can make testing simpler.  Another convention is that constants are defined as class values, not instance values.

## Plus/Minus Infinity

This idea came from the Boost/C++ library, and is included mainly because it makes Intervals so much more powerful.

## Flexible parsing and formatting (marshalling and unmarshalling)

It would be the height of hubris for a designer to think they can predict all the external formats that a programmer might be forced to use, so **chronian** provides simple defaults for the common cases and a range of customization options to handle nearly any other cases.

## Database Interoperability

One of the most common places to read/write dates-and-times are databases, so **chronian** has to provide facilities to do this easily -- even though databases sometimes make assumptions that clash with the very essence of how the Chronian conceptual model works.

## Native Interoperability

If this library is to be useful it obviously must be easy to convert between **chronian** objects and native objects, so we include a full complement of conversion methods.  This is not just for convenience; to ensure that conversions (which often have hidden subtleties) are done correctly they really should be included in the library.  Indeed, it would violate the spirit of **chronian** to require the user to ever manipulate an internal representation of a date-time object.

## Open-Source

No one should own "time", and I'm not looking to make money off this.  (Fame might stroke my ego, but I'm not holding my breath on that one either.)  My goals are (1) to find out if this model works, and (2) to see it widely used if it does work.  Open-source enables both.


---
Copyright (c) 2016-2017 Michael S. Kenniston
