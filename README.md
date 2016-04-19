# chronian

**chronian** is a temporal library, i.e. one for manipulating date-and-time data.  The primary ways in which it differs from other temporal libraries are:

* *Provides cross-language availability and consistency:*  **chronian** is designed from the outset to be implemented in multiple programming languages, and it maintains a uniform API and semantics across all implementations (to the extent reasonable under the constraints of each language).  This is attractive if you routinely code in multiple languages and are tired of memorizing multiple APIs that all do the same thing.
* *Models time zones as the fundamental ADTs:*  The basic conceptual model used by **chronian** is different from that used in more traditional libraries.  Most existing temporal libraries assume that there is a single "real" physical time-line, and that time zones simply represent different mappings of the points on that single time-line into concrete representations (e.g. strings).  **chronian** turns that model on its head, modeling each time zone as its own independent ADT (Abstract Data Type, i.e. a collection of values and operations on those values), each of which is equally "real".  Conversions between time-points in different time zones are considered to be similar to conversions between strings, integers, and floats:  useful, even essential, but best-effort and sometimes lossy.  This model clarifies certain gnarly aspects of temporal logic, making it easier to understand without making the code any more complicated.  For more details, see http://www.chronian.com.
* *Enables simple, concise, and correct handling of time zones:*  A few existing temporal libraries do handle time zones well, but many others handle them poorly, clumsily, or not at all.  **chronian** handles them well.  For example, it avoids troublesome ambiguities by not allowing you to create a date-time without a time zone.

Other notable features of **chronian** include:

* *Immutable date-times:*  In addition to making it easier to reason about date-time objects, making them immutable also makes them MT-safe without the need for any thread-synchronization code.
* *Opaque date-times:*  Many temporal libraries' date-time objects fall short by being implemented as a leaky abstraction:  In order to really predict the results of an operation, you need to know and understand the underlying representation.  This defeats the purpose of abstraction.  **chronian** date-time objects are fully encapsulated:  Their interfaces completely define their behavior, and you need never be concerned with how they're implemented.
* *Clocks as distinct objects*:  Temporal libraries typically include a "now" method as part of the date-time class.  **chronian** keeps the notion of clocks completely distinct from the ADTs that form the basis of temporal computation.  This is not only conceptually cleaner, but it also makes it easier to mock or dependency-inject clocks into automated tests.
* *Compact time zone ids*:  Some contexts demand that date-times be stored together with their time zones, but the official IANA names for time zones can be as long as the ISO-8601 string representation of the entire remainder of the date-time.  **chronian** provides a shorter (4-character) representation that is still based on an international standard (IATA).
* *Distinguishes 3 types of equality:*  Two temporal objects can be "equal" in three ways:  (1) the same object, i.e. pointer equality, (2) the same values, i.e. value equality, and (3) simultaneity, i.e. temporal equality.  **chronian** keeps these distinct and makes explicit which one you're testing.
* *Defines 2 types of ordering:*  There are (or should be) two "<, =, >" relationships defined on temporal objects:  (1) temporal order, based on which point is earlier, and (2) sort order, which allows sorting into consistent order even when objects that are value-unequal are temporally equal.  **chronian** explicitly defines these two orderings.
* *Provides a rich set of customizations:*  There are many details to decide on when defining an abstraction of time, e.g. how leap seconds are treated, which calendar(s) to use, and what restrictions one might place on conversions.  Most temporal libraries make these decisions for you, in ways that may or may not meet your needs.  **chronian** allows you to choose options appropriate to your specific context in a clear, simple way that does not complicate the interface.
* *tzinfo version-aware:*  Virtually every other temporal library assumes that the tzinfo data is constant, yet this is patently false -- in fact those files are updated every few weeks.  This can lead to obscure and thorny problems in traditional temporal processing, but **chronian** allows you to handle this situation clearly and gracefully.
* *Minimizes name-space pollution:*  Once you import the "Chron" class into your namespace, everything else is available from that.

Finally, **chronian** meets the fundamental requirements you'd ask of any library:

* *Complete Documentation:*  Every class, method, argument, and constant is fully documented.
* *Test Coverage:*  The library includes a full suite of automated unit tests to verify the functionality of every method.  The same tests are run on every language implementation.
* *Open Source:*  All the source code is checked into a publicly-readable repository on github.com (https://github.com/mkenniston/chronian).  Feel free to clone it and play.  Better yet, fork it, improve it, and submit a pull request to incorporate your contribution into the master branch.

## Disclaimer

This library is very much a work-in-progress, and it is in its early stages.  It is most definitely *not* production quality, and many of the points described above are *design goals* that have not yet been implemented.

Feedback is welcome, and your good ideas could influence the design.  You can contact me at *mike@chronian.com*.
