.. ifconfig:: calcephapi in ('C')

    ::
    
     int res;
     int j;
     double jd0=2451624;
     double dt1=0.5E0;
     double dt2=0.9E0;
 
     double PV[6];
     /* open the ephemeris file */
     res = calceph_sopen("example1.dat");
     if (res)
     {
       /* the heliocentric coordinates of Mars */
       calceph_scompute(jd0, dt1, 4, 11, PV);
       for(j=0; j<6; j++) printf("%23.16E\n", PV[j]);
   
       calceph_scompute(jd0, dt2, 4, 11, PV);
       for(j=0; j<6; j++) printf("%23.16E\n", PV[j]);
 
       /* close the ephemeris file */
       calceph_sclose();
     }


.. ifconfig:: calcephapi in ('F2003')

    ::
    
           integer res
           real(8) jd0
           real(8) dt1, dt2
           real(8) PV(6)

           jd0 = 2442457
           dt1 = 0.5D0
           dt2 = 0.9D0
           
           res = calceph_sopen("example1.dat"//C_NULL_CHAR)
           if (res.eq.1) then
                ! the heliocentric coordinates of Mars 
                res = calceph_scompute(jd0, dt1, 4, 11, PV)
                write (*,*) PV

                res = calceph_scompute(jd0, dt2, 4, 11, PV)
                write (*,*) PV
          
                call calceph_sclose
           endif     

.. ifconfig:: calcephapi in ('F90')

    ::
    
           double precision PV(6)
           integer res
           double precision jd0
           double precision dt1, dt2

           jd0 = 2442457
           dt  = 0.5D0
           dt2 = 0.9D0
           
           res = f90calceph_sopen("example1.dat")
           if (res.eq.1) then

              ! the heliocentric coordinates of Mars 
              res = f90calceph_scompute(jd0, dt1, 4, 11, PV)
              write (*,*) PV
 
              res = f90calceph_scompute(jd0, dt2, 4, 11, PV)
              write (*,*) PV

             call f90calceph_sclose
           endif  
