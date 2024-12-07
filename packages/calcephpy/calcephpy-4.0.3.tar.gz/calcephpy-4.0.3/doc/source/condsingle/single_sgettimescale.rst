
.. ifconfig:: calcephapi in ('C')

    ::

        int res, timescale;
        calceph_sopen("example1.dat");
        timescale = calceph_sgettimescale();
        printf("timescale : %s\n", timescale==1?"TDB":"TCB");

.. ifconfig:: calcephapi in ('F2003')

    ::
    
           integer res
           integer t
           res = calceph_sopen("example1.dat"//C_NULL_CHAR)
           if (res.eq.1) then
           
             t = calceph_sgettimescale()
             write (*,*) "timescale ", t
             
             call calceph_sclose
           endif
       

.. ifconfig:: calcephapi in ('F90')

    ::
    
           integer res
           integer t
           ! open the ephemeris file 
           res = f90calceph_sopen("example1.dat")
           if (res.eq.1) then
           
               t = f90calceph_sgettimescale()
               write (*,*) "timescale ", t

               call f90calceph_sclose
           endif
      
