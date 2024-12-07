.. @c %----------------------------------------------------------------------------

.. include:: ../replace.rst

Single file access functions
============================

.. ifconfig:: calcephapi in ('Python')

    .. warning::
        The python interface does not provide these functions, the listed in the section :ref:`Multiple file access functions`  must be used.


.. @c .. warning::
    
.. @c .. deprecated:: 3.0 
.. @c Use :ref:`Multiple file access functions` instead.

This group of functions works on a single ephemeris file at a given instant. 
They use an internal global variable to store information about the current opened ephemeris file. 

They are provided to have a similar interface of the fortran PLEPH function, supplied with the JPL ephemeris files. 
So the following call to PLEPH


.. code-block:: fortran
    
        PLEPH(46550D0, 3, 12, PV)
        

could be replaced by

.. code-block:: fortran
        
        calceph_sopen("ephemerisfile.dat")
        calceph_scompute(46550D0, 0, 3, 12, PV)
        calceph_sclose()


While the function PLEPH could access only one file in a program, these functions could access on multiple files in a program but not at same time. To access multiple files at a same time, the functions listed in the section :ref:`Multiple file access functions`  must be used.  

When an error occurs, these functions execute error handlers according to the behavior defined by the function |calceph_seterrorhandler|. 


The python interface does not provide these functions, the listed in the section :ref:`Multiple file access functions`  must be used.

Time notes
----------

The function |calceph_scompute| only accepts a date expressed in the same timescale as the ephemeris files, which can be retrieved using the function |calceph_sgettimescale|. Ephemeris files are generally expressed using the timescale TDB.
If a date, expressed in the TT (Terrestrial Time) timescale, is supplied to this function, |calceph_scompute| will return an erroneous position of the order of several tens of meters for the planets.
If a date, expressed in the Coordinated Universal Time (UTC), is supplied to this function, |calceph_scompute| will return a very large erroneous position over several thousand kilometers for the planets.

  
Thread notes
------------

If the standard I/O functions such as *fread* are not reentrant
then the |LIBRARYSHORTNAME| I/O functions using them will not be reentrant either.

If the library was configured with the option *--enable-thread=yes*,
these functions use an internal global variable per thread. Each thread could access to different ephemeris file and compute ephemeris data at same time. But each thread must call the function |calceph_sopen| to open ephemeris file even if all threads work on the same file.

If the library was configured with the default option *--enable-thread=no*,
these functions use an internal global variable per process and are not thread-safe. If multiple threads are used in the process and call the function |calceph_scompute| at the same time, the caller thread must surround the call to this function with locking primitives, such as *pthread_lock/pthread_unlock* if POSIX Pthreads are used. 


Usage
-----

The following examples, that can be found in the directory *examples* of the library sources, show the typical usage of this group of functions. 

.. ifconfig:: calcephapi in ('C')

    The example in C language is :file:`csingle.c`. 
    
.. ifconfig:: calcephapi in ('F2003')

    The example in Fortran 2003 language is :file:`f2003single.f`.
    
.. ifconfig:: calcephapi in ('F90')

    The example in Fortran 77/90/95 language is :file:`f77single.f`.


.. include:: single_prog.rst


Functions
---------

|menu_calceph_sopen|
~~~~~~~~~~~~~~~~~~~~

.. ifconfig:: calcephapi in ('C')

    
    .. c:function:: int calceph_sopen ( const char *filename)

        :param filename: |arg_filename|
        :return: |retfuncfails0|


.. ifconfig:: calcephapi in ('F2003')

    .. f:function:: calceph_sopen (filename) BIND(C)

        :p  filename [CHARACTER(len=1,kind=C_CHAR), intent(in)]: |arg_filename|.
        :r calceph_sopen: |retfuncfails0|
        :rtype calceph_sopen: INTEGER(C_INT)

.. ifconfig:: calcephapi in ('F90')

    .. f:function:: f90calceph_sopen (filename)

        :p  filename [CHARACTER(len=*), intent(in)]: |arg_filename|.
        :r f90calceph_sopen: |retfuncfails0|
        :rtype f90calceph_sopen: INTEGER


This function opens the file whose pathname is the string pointed to by filename, reads the header of this file
and associates an ephemeris descriptor to an internal variable. 
This file must be an ephemeris file.

This file must be compliant to the format specified by the  'original JPL binary' , 'INPOP 2.0 binary' or 'SPICE' ephemeris file. 
At the moment, supported SPICE files are the following :


 * text Planetary Constants Kernel (KPL/PCK) files
 * binary PCK  (DAF/PCK) files.
 * binary SPK (DAF/SPK) files containing segments of type |supportedspk|.
 * meta kernel (KPL/MK) files.
 * frame kernel (KPL/FK) files. Only a basic support is provided.

The function |calceph_sclose| must be called to free allocated memory by this function.

The following example opens the ephemeris file example1.dat 

.. ifconfig:: calcephapi in ('C')

 ::
 
     int res;
     res = calceph_sopen("example1.dat");
     if (res)
     {
       /* 
         ...  computation ... 
       */
       calceph_sclose();
     }

.. ifconfig:: calcephapi in ('F2003')

 ::

           integer res
           res = calceph_sopen("example1.dat"//C_NULL_CHAR)
           if (res.eq.1) then
                ! ...  computation ... 
           endif
           call calceph_sclose     

.. ifconfig:: calcephapi in ('F90')

 ::

           integer res
           res = f90calceph_sopen("example1.dat")
           if (res.eq.1) then
                ! ...  computation ... 
           endif
           call f90calceph_sclose     

.. %------------------------------------------------

|menu_calceph_scompute|
~~~~~~~~~~~~~~~~~~~~~~~

.. ifconfig:: calcephapi in ('C')

    .. c:function:: int calceph_scompute ( double JD0, double time, int target, int center, double PV[6] )

        :param  JD0: |arg_JD0|
        :param  time: |arg_time|
        :param  target: |arg_target|
        :param  center: |arg_center|
        :param  PV:  .. include:: ../arg_PV.rst
        :return: |retfuncfails0|

.. ifconfig:: calcephapi in ('F2003')

    .. f:function:: calceph_scompute (JD0, time, target, center, PV) BIND(C)

        :param JD0 [REAL(C_DOUBLE), VALUE, intent(in)]: |arg_JD0|
        :param time [REAL(C_DOUBLE), VALUE, intent(in)]: |arg_time|
        :param target [INTEGER(C_INT), VALUE, intent(in)]: |arg_target|
        :param center [INTEGER(C_INT), VALUE, intent(in)]: |arg_center|
        :param PV[REAL(C_DOUBLE), dimension(1\:6), intent(out)]: .. include:: ../arg_PV.rst
        :r calceph_scompute: |retfuncfails0|
        :rtype calceph_scompute: INTEGER(C_INT)


.. ifconfig:: calcephapi in ('F90')

    .. f:function:: f90calceph_scompute (JD0, time, target, center, PV)

        :param JD0 [REAL(8), intent(in)]: |arg_JD0|
        :param time [REAL(8), intent(in)]: |arg_time|
        :param target [INTEGER, intent(in)]: |arg_target|
        :param center [INTEGER, intent(in)]: |arg_center|
        :param PV(6) [REAL(8), intent(out)]: .. include:: ../arg_PV.rst
        :r f90calceph_scompute: |retfuncfails0|
        :rtype f90calceph_scompute: INTEGER


This function reads, if needed, and interpolates a single object, usually the position and velocity of one body (*target*) relative to another (*center*), from the ephemeris file, previously opened with the function |calceph_sopen|, for the time *JD0+time* and stores the results to *PV*. 


The date (JD0, time) should be expressed in the same timescale as the ephemeris files, which can be retrieved using the function |calceph_sgettimescale|.  

.. warning::
    If a date, expressed in the Coordinated Universal Time (UTC), is supplied to this function, a very large erroneous position will be returned. 


To get the best precision for the interpolation, the time is splitted in two floating-point numbers. The argument *JD0* should be an integer and *time* should be a fraction of the day. But you may call this function with *time=0* and *JD0*, the desired time, if you don't take care about precision.


The possible values for *target* and *center* are  :

+------------------------------------+------------------------+
| value                              |            meaning     |
+====================================+========================+
| 1                                  | Mercury Barycenter     |
+------------------------------------+------------------------+
| 2                                  | Venus Barycenter       |
+------------------------------------+------------------------+
| 3                                  | Earth                  |
+------------------------------------+------------------------+
| 4                                  | Mars Barycenter        |
+------------------------------------+------------------------+
| 5                                  | Jupiter Barycenter     |
+------------------------------------+------------------------+
| 6                                  | Saturn Barycenter      |
+------------------------------------+------------------------+
| 7                                  | Uranus Barycenter      |
+------------------------------------+------------------------+
| 8                                  | Neptune Barycenter     |
+------------------------------------+------------------------+
| 9                                  | Pluto Barycenter       |
+------------------------------------+------------------------+
| 10                                 | Moon                   |
+------------------------------------+------------------------+
| 11                                 | Sun                    |
+------------------------------------+------------------------+
| 12                                 | Solar Sytem barycenter |
+------------------------------------+------------------------+
| 13                                 | Earth-moon barycenter  |
+------------------------------------+------------------------+
| 14                                 | Nutations              |
+------------------------------------+------------------------+
| 15                                 | Librations             |
+------------------------------------+------------------------+
| 16                                 | TT-TDB                 |
+------------------------------------+------------------------+
| 17                                 | TCG-TCB                |
+------------------------------------+------------------------+
| asteroid number + CALCEPH_ASTEROID | asteroid               |
+------------------------------------+------------------------+

These accepted values by this function are the same as the value for the JPL function *PLEPH*, except for the values *TT-TDB*, *TCG-TCB* and asteroids.

For example, the value "CALCEPH_ASTEROID+4" for target or center specifies the asteroid Vesta.

The following example prints the heliocentric coordinates of Mars at time=2451624.5 and at 2451624.9 

.. include :: single_scompute.rst


.. %------------------------------------------------

|menu_calceph_sgetconstant|
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. ifconfig:: calcephapi in ('C')

    .. c:function:: int calceph_sgetconstant ( const char* name, double *value )

        :param  name: |arg_constant_name|
        :param  value: |arg_constant_value|
        :return: |retfuncfails0|

.. ifconfig:: calcephapi in ('F2003')

    .. f:function:: calceph_sgetconstant (name, value) BIND(C)

        :p  name [CHARACTER(len=1,kind=C_CHAR), intent(in)]: |arg_constant_name|.
        :p  value [REAL(C_DOUBLE), intent(out)]: |arg_constant_value|.
        :r calceph_getconstant: |retfuncfails0|
        :rtype calceph_getconstant: INTEGER(C_INT)

.. ifconfig:: calcephapi in ('F90')

    .. f:function:: f90calceph_sgetconstant (name, value ) 

        :p  name  [CHARACTER(len=*), intent(in)]: |arg_constant_name|
        :p  value [REAL(8), intent(out)]: |arg_constant_value|
        :r f90calceph_sgetconstant: |retfuncfails0|
        :rtype f90calceph_sgetconstant: INTEGER

This function returns the value associated to the constant *name* in the header of the ephemeris file.

Only the first value is returned if multiple values are associated to a constant, such as a list of values.

The function |calceph_sopen| must be previously called  before.

The following example prints the value of the astronomical unit stored in the ephemeris file

.. include :: single_sgetconstant.rst


.. %------------------------------------------------

|menu_calceph_sgetconstantcount|
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. ifconfig:: calcephapi in ('C')

    .. c:function:: int calceph_sgetconstantcount ( )

        :return: |retfuncfails0|

.. ifconfig:: calcephapi in ('F2003')

    .. f:function:: calceph_sgetconstantcount () BIND(C)

        :r calceph_sgetconstantcount: |retfuncfails0|
        :rtype calceph_sgetconstantcount: INTEGER(C_INT)

.. ifconfig:: calcephapi in ('F90')

    .. f:function:: f90calceph_sgetconstantcount () 

        :r f90calceph_prefetch: |retfuncfails0|
        :rtype f90calceph_sgetconstantcount: INTEGER

This function returns the number of constants available in the header of the ephemeris file.

The function |calceph_sopen| must be previously called  before.

The following example prints the number of available constants stored in the ephemeris file

.. include :: single_sgetconstantcount.rst


.. %------------------------------------------------

|menu_calceph_sgetconstantindex|
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. ifconfig:: calcephapi in ('C')

    .. c:function:: int calceph_sgetconstantindex ( int index, char name[CALCEPH_MAX_CONSTANTNAME], double *value)

        :param  index: |arg_constant_index|
        :param  name: |arg_constant_name|
        :param  value: |arg_constant_value|
        :return: |retfuncfails0|

.. ifconfig:: calcephapi in ('F2003')

    .. f:function:: calceph_sgetconstantindex (index, name, value) BIND(C)

        :p  index [INTEGER(C_INT), VALUE, intent(in)]: |arg_constant_index|
        :p  name [CHARACTER(len=1,kind=C_CHAR),  dimension(CALCEPH_MAX_CONSTANTNAME), intent(out)]: |arg_constant_name|.
        :p  value [REAL(C_DOUBLE), intent(out)]: |arg_constant_value|
        :r calceph_sgetconstantindex: |retfuncfails0|
        :rtype calceph_sgetconstantindex: INTEGER(C_INT)

.. ifconfig:: calcephapi in ('F90')

    .. f:function:: f90calceph_sgetconstantindex (index, name, value) 

        :p  index [INTEGER, intent(in)]: |arg_constant_index|
        :p  name  [CHARACTER(len=CALCEPH_MAX_CONSTANTNAME), intent(out)]: |arg_constant_name|
        :p  value [REAL(8), intent(out)]: |arg_constant_value|
        :r f90calceph_sgetconstantindex: |retfuncfails0|
        :rtype f90calceph_sgetconstantindex: INTEGER


This function returns the name and its value of the constant available at the specified index in the header of the ephemeris file. The value of *index* must be between 1 and |calceph_sgetconstantcount|.

.. ifconfig:: calcephapi in ('F90')

    Trailing blanks are added to the name of the constant.

The function |calceph_sopen| must be previously called before.


The following example displays the name of the constants, stored in the ephemeris file, and their values 

.. include :: single_sgetconstantindex.rst

.. %------------------------------------------------

|menu_calceph_sgetfileversion|
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 


.. ifconfig:: calcephapi in ('C')

    .. c:function:: int calceph_sgetfileversion ( char version[CALCEPH_MAX_CONSTANTVALUE])

        :param  version: |arg_fileversion|
        :return: |retfuncnotfound0|

.. ifconfig:: calcephapi in ('F2003')

    .. f:function:: calceph_sgetfileversion (version) BIND(C)
    
        :param  version [CHARACTER(len=1,kind=C_CHAR), dimension(CALCEPH_MAX_CONSTANTVALUE), intent(out)]: |arg_fileversion|
        :r calceph_sgetfileversion: |retfuncnotfound0|
        :rtype calceph_sgetfileversion: INTEGER(C_INT)

.. ifconfig:: calcephapi in ('F90')

     .. f:function:: f90calceph_sgetfileversion (version) 
     
        :param  version [CHARACTER(len=CALCEPH_MAX_CONSTANTVALUE), intent(out)]: |arg_fileversion|
        :r f90calceph_sgetfileversion: |retfuncnotfound0|
        :rtype f90calceph_sgetfileversion: INTEGER


This function returns the version of the ephemeris file, as a string. For example, the argument version will contain 'INPOP10B', 'EPM2017' or 'DE405', ... . 

If the file is an original JPL binary planetary ephemeris, then the version of the file can always be determined.
If the file is a spice kernel, the version of the file is retrieved from the constant *INPOP_PCK_VERSION*, *EPM_PCK_VERSION*, or *PCK_VERSION*.

The function |calceph_sopen| must be previously called before.

The following example prints the version of the ephemeris file. 

.. include:: single_sgetfileversion.rst

.. %------------------------------------------------

|menu_calceph_sgettimescale|
~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

.. ifconfig:: calcephapi in ('C')

    .. c:function:: int calceph_sgettimescale ()

        :return: |retfuncfails0|

.. ifconfig:: calcephapi in ('F2003')

    .. f:function:: calceph_sgettimescale () BIND(C)

        :r calceph_sgettimescale: |retfuncfails0|
        :rtype calceph_sgettimescale: INTEGER(C_INT)

.. ifconfig:: calcephapi in ('F90')

    .. f:function:: f90calceph_sgettimescale () 

        :r f90calceph_sgettimescale: |retfuncfails0|
        :rtype f90calceph_sgettimescale: INTEGER

This function returns the timescale of the ephemeris file : 
  * 1 if the quantities of all bodies are expressed in the TDB time scale. 
  * 2 if the quantities of all bodies are expressed in the TCB time scale. 
  
The function |calceph_sopen| must be previously called before.

The following example prints the time scale available in the ephemeris file

.. include:: single_sgettimescale.rst

.. %------------------------------------------------

|menu_calceph_sgettimespan|
~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

.. ifconfig:: calcephapi in ('C')

    .. c:function:: int calceph_sgettimespan (double* firsttime, double* lasttime, int* continuous )

        :param  firsttime: |arg_firsttime|
        :param  lasttime: |arg_lasttime|
        :param  continuous: |arg_continuous|
        :return: |retfuncfails0|

.. ifconfig:: calcephapi in ('F2003')

    .. f:function:: calceph_sgettimespan (firsttime, lasttime, continuous) BIND(C)

        :param firsttime [REAL(C_DOUBLE), intent(out)]: |arg_firsttime|
        :p  lasttime [REAL(C_DOUBLE), intent(out)]: |arg_lasttime|
        :p  continuous [INTEGER(C_INT), intent(out)]: |arg_continuous|
        :r calceph_sgettimespan: |retfuncfails0|
        :rtype calceph_sgettimespan: INTEGER(C_INT)

.. ifconfig:: calcephapi in ('F90')

    .. f:function:: f90calceph_sgettimespan (firsttime, lasttime, continuous) 

        :param firsttime [REAL(8), intent(out)]: |arg_firsttime|
        :p  lasttime [REAL(8), intent(out)]: |arg_lasttime|
        :p  continuous [INTEGER, intent(out)]: |arg_continuous|
        :r f90calceph_sgettimespan: |retfuncfails0|
        :rtype f90calceph_sgettimespan: INTEGER

This function returns the first and last time available in the ephemeris file. The Julian date for the first and last time are expressed in the time scale returned by  |calceph_sgettimescale|
. 

It returns the following value in the parameter *continuous* :

  * 1 if the quantities of all bodies are available for any time between the first and last time. 
  * 2 if the quantities of some bodies are available on discontinuous time intervals between the first and last time. 
  * 3 if the quantities of each body are available on a continuous time interval between the first and last time, but not available for any time between the first and last time. 
  
The function |calceph_sopen| must be previously called before.

The following example prints the first and last time available in the ephemeris file

.. include:: single_sgettimespan.rst

.. %------------------------------------------------

|menu_calceph_sclose|
~~~~~~~~~~~~~~~~~~~~~

.. ifconfig:: calcephapi in ('C')

    .. c:function:: void calceph_sclose ( )
    
.. ifconfig:: calcephapi in ('F2003')

    .. f:subroutine:: calceph_sclose ( )

.. ifconfig:: calcephapi in ('F90')

    .. f:subroutine:: f90calceph_sclose ( )

This function closes the ephemeris data file and frees allocated memory by the function |calceph_sopen|.

