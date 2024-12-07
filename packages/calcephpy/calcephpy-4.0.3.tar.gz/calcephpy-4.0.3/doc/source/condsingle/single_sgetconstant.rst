.. ifconfig:: calcephapi in ('C')

    ::
    
        int res;
        double UA;
        calceph_sopen("example1.dat");
        res = calceph_sgetconstant("UA",&UA);
        if (res) 
        {
           printf("astronomical unit=%23.16E\n", UA);
        }

.. ifconfig:: calcephapi in ('F2003')

    ::
    
           integer res
           real(8) AU
           ! open the ephemeris file 
           res = calceph_sopen("example1.dat"//C_NULL_CHAR)
           if (res.eq.1) then
               if (calceph_sgetconstant("AU"//C_NULL_CHAR, AU).eq.1) then
                   write (*,*) "AU=", AU
               endif
           endif
       

.. ifconfig:: calcephapi in ('F90')

    ::
    
           integer res
           double precision AU

           res = f90calceph_sopen("example1.dat")
           if (res.eq.1) then
               if (f90calceph_sgetconstant("AU", AU).eq.1) then
                   write (*,*) "AU=", AU
               endif
            endif
      
