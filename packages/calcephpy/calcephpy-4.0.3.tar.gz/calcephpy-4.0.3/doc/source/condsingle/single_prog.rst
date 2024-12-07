.. ifconfig:: calcephapi in ('C')

    ::
    
        #include <stdio.h>
        #include "calceph.h"

        /*-----------------------------------------------------------------*/
        /* main program */
        /*-----------------------------------------------------------------*/
        int main()
        {
         int res;
         double AU, EMRAT, GM_Mer;
         double jd0=2451624;
         double dt=0.5E0;
         double PV[6];

         /* open the ephemeris file */
         res = calceph_sopen("example1.dat");
         if (res)
         {
            printf("The ephemeris is already opened\n");
           /* print the values of AU, EMRAT and GM_Mer */
           if (calceph_sgetconstant("AU", &AU)) 
               printf("AU=%23.16E\n", AU);
   
           if (calceph_sgetconstant("EMRAT", &EMRAT)) 
             printf("EMRAT=%23.16E\n", EMRAT);
   
           if (calceph_sgetconstant("GM_Mer", &GM_Mer)) 
             printf("GM_Mer=%23.16E\n", GM_Mer);
 
           /* compute and print the coordinates */
           /* the geocentric moon coordinates in AU and AU/day */
           calceph_scompute(jd0, dt, 10, 3, PV);
           printcoord(PV,"geocentric coordinates of the Moon in AU and AU/day");
   
           /* the value TT-TDB */
           calceph_scompute(jd0, dt, 16, 0, PV);
           printf("TT-TDB = %23.16E\n", PV[0]);
   
           /* the heliocentric coordinates of Mars */
           calceph_scompute(jd0, dt, 4, 11, PV);
           printcoord(PV,"heliocentric coordinates of Mars");
 
           /* close the ephemeris file */
           calceph_sclose();
           printf("The ephemeris is already closed\n");
         }
         else
         {
           printf("The ephemeris can't be opened\n");
         }
         return res;
        }
        
.. ifconfig:: calcephapi in ('F2003')

    ::
    
         USE, INTRINSIC :: ISO_C_BINDING
         use calceph
         implicit none
         integer res
         real(8) AU, EMRAT, GM_Mer
         real(8) jd0
         real(8) dt
         real(8) PV(6)
         integer j
         real(8) valueconstant
         character(len=CALCEPH_MAX_CONSTANTNAME) nameconstant

         jd0 = 2442457
         dt = 0.5E0
         ! open the ephemeris file 
         res = calceph_sopen("example1.dat"//C_NULL_CHAR)
         if (res.eq.1) then
           write (*,*) "The ephemeris is already opened"
           ! print the values of AU, EMRAT and GM_Mer 
           if (calceph_sgetconstant("AU"//C_NULL_CHAR, AU).eq.1) then
               write (*,*) "AU=", AU
           endif
           if (calceph_sgetconstant("EMRAT"//C_NULL_CHAR,EMRAT).eq.1) then
               write (*,*) "EMRAT=", EMRAT
           endif
           if (calceph_sgetconstant("GM_Mer"//C_NULL_CHAR,GM_Mer).eq.1) then
               write (*,*) "GM_Mer=", GM_Mer
           endif

           ! compute and print the coordinates 
           ! the geocentric moon coordinates 
           res = calceph_scompute(jd0, dt, 10, 3, PV)
           call printcoord(PV,"geocentric coordinates of the Moon")
           ! the value TT-TDB 
           if (calceph_scompute(jd0, dt, 16, 0, PV).eq.1) then
             write (*,*) "TT-TDB = ", PV(1)
           endif
           ! the heliocentric coordinates of Mars 
           res = calceph_scompute(jd0, dt, 4, 11, PV)
           call printcoord(PV,"heliocentric coordinates of Mars")


           ! print the whole list of the constants 
           write (*,*) "list of constants"
           do j=1, calceph_sgetconstantcount()
             res = calceph_sgetconstantindex(j,nameconstant, valueconstant)
             write (*,*) nameconstant,"=",valueconstant
           enddo


           ! close the ephemeris file 
           call calceph_sclose
           write (*,*) "The ephemeris is already closed"
         else
           write (*,*) "The ephemeris can't be opened"
         endif
       

.. ifconfig:: calcephapi in ('F90')

    ::
    
       program f77single
           implicit none
           include 'f90calceph.h'
           integer res
           double precision AU, EMRAT, GM_Mer
           double precision jd0
           double precision dt
           double precision PV(6)
           integer j
           double precision valueconstant
           character(len=CALCEPH_MAX_CONSTANTNAME) nameconstant

           jd0 = 2442457
           dt = 0.5E0
           ! open the ephemeris file 
           res = f90calceph_sopen("example1.dat")
           if (res.eq.1) then
               write (*,*) "The ephemeris is already opened"
               ! print the values of AU, EMRAT and GM_Mer 
               if (f90calceph_sgetconstant("AU", AU).eq.1) then
                   write (*,*) "AU=", AU
               endif
               if (f90calceph_sgetconstant("EMRAT", EMRAT).eq.1) then
                   write (*,*) "EMRAT=", EMRAT
               endif
               if (f90calceph_sgetconstant("GM_Mer", GM_Mer).eq.1)then
                   write (*,*) "GM_Mer=", GM_Mer
               endif
 
              ! compute and print the coordinates 
              ! the geocentric moon coordinates 
              res = f90calceph_scompute(jd0, dt, 10, 3, PV)
              call printcoord(PV,"geocentric coordinates of the Moon")
              ! the value TT-TDB 
              if (f90calceph_scompute(jd0, dt, 16, 0, PV).eq.1) then
               write (*,*) "TT-TDB = ", PV(1)
              endif
              ! the heliocentric coordinates of Mars 
              res = f90calceph_scompute(jd0, dt, 4, 11, PV)
              call printcoord(PV,"heliocentric coordinates of Mars")
 
             ! print the whole list of the constants 
             write (*,*) "list of constants"
             do j=1, f90calceph_sgetconstantcount()
                res = f90calceph_sgetconstantindex(j,nameconstant,valueconstant)
                write (*,*) nameconstant,"=",valueconstant
             enddo

             ! close the ephemeris file 
             call f90calceph_sclose
             write (*,*) "The ephemeris is already closed"
            else
               write (*,*) "The ephemeris can't be opened"
            endif
       stop
       end
      
