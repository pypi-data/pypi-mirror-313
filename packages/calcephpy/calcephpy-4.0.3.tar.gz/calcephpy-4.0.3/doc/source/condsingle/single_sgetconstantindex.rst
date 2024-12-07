.. ifconfig:: calcephapi in ('C')

    ::
    
         int j;
         int res;
         char nameconstant[CALCEPH_MAX_CONSTANTNAME];
         double valueconstant;

         res = calceph_sopen("example1.dat");
         if (res)
         {
             for (j=1; j<=calceph_sgetconstantcount(); j++)
             {
                 calceph_sgetconstantindex(j, nameconstant, &valueconstant);
                 printf("'%s'\t= %23.16E\n", nameconstant, valueconstant);
             }
             calceph_sclose();
         }


.. ifconfig:: calcephapi in ('F2003')

    ::
    
           integer res
           integer j
           real(8) valueconstant
           character(len=CALCEPH_MAX_CONSTANTNAME) nameconstant

           res = calceph_sopen("example1.dat"//C_NULL_CHAR)
           if (res.eq.1) then

             do j=1, calceph_sgetconstantcount()
               res = calceph_sgetconstantindex(j,nameconstant,valueconstant)
               write (*,*) nameconstant,"=",valueconstant
             enddo

           call calceph_sclose


.. ifconfig:: calcephapi in ('F90')

    ::
    
           integer res
           integer j
           double precision valueconstant
           character(len=CALCEPH_MAX_CONSTANTNAME) nameconstant

           res = f90calceph_sopen("example1.dat")
           if (res.eq.1) then
           
             do j=1, f90calceph_sgetconstantcount()
                res = f90calceph_sgetconstantindex(j,nameconstant,valueconstant)
                write (*,*) nameconstant,"=",valueconstant
             enddo
             
             call f90calceph_sclose
           endif

