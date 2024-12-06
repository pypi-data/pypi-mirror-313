Annual reporting
================================

In terms of the annual reporting, the core of the wrap_technote package is arranged around
three concepts:

1. Reporting period. This is essentially a "round" of reporting, and for example,
   "2019-20" refers to the reporting done in the 2019-20 financial year, traditionally
   done in early 2020, using the data collected in the spring 2019 monitoring rounds.
   This also refers to a single folder path, under which all the data, scripts, and
   results are stored.

2. Report. This correlates directly to a Technical Note. More on this below.

3. Resource. This represents a set of wells being monitored for either water level, or
   for salinity (i.e. there will be one resource for water level data, and one resource
   for salinity data).

More on these below!

Reporting period
----------------

Fundamentally a reporting period is a folder path, which should be called "Code". It is
referred to in the code as either a string e.g. `"2019-20"`, or a 
:class:`wrap_technote.ReportingPeriod` object. The mapping from the shorthand string to
the folder path is found in the :attr:`wrap_technote.reporting.reporting_period_paths`
module attribute.

Report
------

#TODO

Resource
--------

#TODO

