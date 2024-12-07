
.. ifconfig:: calcephapi in ('C')

    ::

        int res;
        double jdfirst, jdlast;
        int cont;
        calceph_sopen("example1.dat");
        res = calceph_sgettimespan(&jdfirst, &jdlast, &cont);
        printf("data available between [ %f, %f ]. continuous=%d\n", 
               jdfirst, jdlast, cont);

.. ifconfig:: calcephapi in ('F2003')

    ::
    
           integer res
           integer cont
           real(8) jdfirst, jdlast
           res = calceph_sopen("example1.dat"//C_NULL_CHAR)
           if (res.eq.1) then
           
             res = calceph_sgettimespan(jdfirst, jdlast, cont)
             write (*,*) "data available between ", jdfirst, "and", jdlast
             write (*,*) "continuous data ", cont
             
             call calceph_sclose
           endif
       

.. ifconfig:: calcephapi in ('F90')

    ::
    
           integer res
           integer cont
           double precision  jdfirst, jdlast
           ! open the ephemeris file 
           res = f90calceph_sopen("example1.dat")
           if (res.eq.1) then
           
             res = f90calceph_sgettimespan(jdfirst, jdlast, cont)
             write (*,*) "data available between ", jdfirst, "and", jdlast
             write (*,*) "continuous data ", cont

               call f90calceph_sclose
           endif
      
