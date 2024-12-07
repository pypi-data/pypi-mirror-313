Introduction 
************


The |LIBRARYNAME| is designed to access the binary planetary ephemeris files, such INPOPxx and JPL DExxx ephemeris files, (called 'original JPL binary'  or 'INPOP 2.0 or 3.0 binary' ephemeris files in the next sections) and the SPICE kernel files  (called 'SPICE' ephemeris files in the next sections). 
At the moment, supported SPICE files are  :

 * text Planetary Constants Kernel (KPL/PCK) files
 * binary PCK  (DAF/PCK) files.
 * binary SPK (DAF/SPK) files containing segments of type |supportedspk|.
 * meta kernel (KPL/MK) files.
 * frame kernel (KPL/FK) files. Only a basic support is provided.

This library provides a C interface and, optionally, the Fortran 77 or 2003, Python and Octave/Matlab interfaces, to be called by the application. 

.. ifconfig:: calcephapi in ('C', 'F2003', 'F90')

    Two groups of functions enable the access to the ephemeris files : 

     * Multiple file access functions

        These functions provide access to many ephemeris file at the same time.


     * Single file access functions

        These functions provide access to only one ephemeris file at the same time. They are provided to make transition easier from the JPL functions, such as *PLEPH*, to this library.


This library could access to the following ephemeris

    * INPOP06 or later
    * DE200        
    * DE403 or later 
    * EPM2011 or later       

Although computers have different endianess (order in which integers are stored as bytes in computer memory), the library could handle the binary ephemeris files with any endianess. This library automatically swaps the bytes when it performs read operations on the ephemeris file.


The internal format of the original JPL binary planetary ephemeris files is described in the paper :

 * David Hoffman : 1998, A Set of C Utility Programs for Processing JPL Ephemeris Data,
   ftp://ssd.jpl.nasa.gov/pub/eph/export/C-versions/hoffman/EphemUtilVer0.1.tar


The 'INPOP 2.0 binary' file format  for  planetary ephemeris files is described in the paper :

 * M. Gastineau, J. Laskar, A. Fienga, H. Manche : 2012,  INPOP binary ephemeris file format - version 2.0
   https://www.imcce.fr/inpop/inpop_file_format_2_0.pdf

The 'INPOP 3.0 binary' file format  for  planetary ephemeris files is described in the paper :

 * M. Gastineau, J. Laskar, A. Fienga, H. Manche : 2017,  INPOP binary ephemeris file format - version 3.0
   https://www.imcce.fr/inpop/inpop_file_format_3_0.pdf
