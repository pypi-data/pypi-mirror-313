This function returns, as a string of character, the value associated to the constant *name* in the header of the ephemeris file |eph|. Only the first value is returned if multiple values are associated to a constant, such as a list of values. The value must be a string, otherwise an error is reported. 

.. ifconfig:: calcephapi in ('F90', 'F2003')

    Trailing blanks are added to each value.

The following example prints the value of the unit stored in the ephemeris file

.. include:: examples/multiple_getconstantss.rst