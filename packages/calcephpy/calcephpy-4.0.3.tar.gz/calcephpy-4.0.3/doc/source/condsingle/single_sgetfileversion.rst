
.. ifconfig:: calcephapi in ('C')

    ::

        int res;
        char version[CALCEPH_MAX_CONSTANTVALUE];
        calceph_sopen("example1.dat");
        res = calceph_sgetfileversion(version);
        printf("The version of the file is %s\n", version);

.. ifconfig:: calcephapi in ('F2003')

    ::
    
           integer res
           character(len=CALCEPH_MAX_CONSTANTVALUE) version
           res = calceph_sopen("example1.dat"//C_NULL_CHAR)
           if (res.eq.1) then
           
             res = calceph_sgetfileversion(version)
             write (*,*) "The version of the file is ", version
             
             call calceph_sclose
           endif
       

.. ifconfig:: calcephapi in ('F90')

    ::
    
           integer res
           character(len=CALCEPH_MAX_CONSTANTVALUE) version
           ! open the ephemeris file 
           res = f90calceph_sopen("example1.dat")
           if (res.eq.1) then
           
             res = f90calceph_sgetfileversion(version)
             write (*,*) "The version of the file is ", version

             call f90calceph_sclose
           endif
      
