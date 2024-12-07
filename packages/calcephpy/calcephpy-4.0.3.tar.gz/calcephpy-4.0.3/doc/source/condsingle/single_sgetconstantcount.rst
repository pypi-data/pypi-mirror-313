
.. ifconfig:: calcephapi in ('C')

    ::

        int res, count;
        calceph_sopen("example1.dat");
        count = calceph_sgetconstantcount();
        printf("number of constants : %d\n", count);

.. ifconfig:: calcephapi in ('F2003')

    ::
    
           integer res
           integer n
           res = calceph_sopen("example1.dat"//C_NULL_CHAR)
           if (res.eq.1) then
           
             n = calceph_sgetconstantcount()
             write (*,*) "number of constants", n
             
             call calceph_sclose
           endif
       

.. ifconfig:: calcephapi in ('F90')

    ::
    
           integer res
           integer n
           ! open the ephemeris file 
           res = f90calceph_sopen("example1.dat")
           if (res.eq.1) then
           
               n = f90calceph_sgetconstantcount()
               write (*,*) "number of constants", n

               call f90calceph_sclose
           endif
      
