#/*-----------------------------------------------------------------*/
#/*! 
#  \file CMakeLists.txt
#  \brief build chain of the tests for cmake. 
#  \author  M. Gastineau 
#           Astronomie et Systemes Dynamiques, IMCCE, CNRS, Observatoire de Paris. 
#
#   Copyright, 2021-2024, CNRS
#   email of the author : Mickael.Gastineau@obspm.fr
#  
#*/
#/*-----------------------------------------------------------------*/
#
#/*-----------------------------------------------------------------*/
#/* License  of this file :
#  This file is "triple-licensed", you have to choose one  of the three licenses 
#  below to apply on this file.
#  
#     CeCILL-C
#     	The CeCILL-C license is close to the GNU LGPL.
#     	( http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html )
#   
#  or CeCILL-B
#        The CeCILL-B license is close to the BSD.
#        (http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.txt)
#  
#  or CeCILL v2.1
#       The CeCILL license is compatible with the GNU GPL.
#       ( http://www.cecill.info/licences/Licence_CeCILL_V2.1-en.html )
#  
# 
# This library is governed by the CeCILL-C, CeCILL-B or the CeCILL license under 
# French law and abiding by the rules of distribution of free software.  
# You can  use, modify and/ or redistribute the software under the terms 
# of the CeCILL-C,CeCILL-B or CeCILL license as circulated by CEA, CNRS and INRIA  
# at the following URL "http://www.cecill.info". 
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability. 
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or 
# data to be ensured and,  more generally, to use and operate it in the 
# same conditions as regards security. 
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL-C,CeCILL-B or CeCILL license and that you accept its terms.
# */
# /*-----------------------------------------------------------------*/



include_directories("${CMAKE_CURRENT_SOURCE_DIR}/../src")
include_directories(${CMAKE_CURRENT_BINARY_DIR})

add_library(calcephtest openfiles.c numericalderivative.c)
target_link_libraries (calcephtest calceph ${LIBM_LIBRARIES})

file(REMOVE "${CMAKE_CURRENT_BINARY_DIR}/example1_tests_23_derivative.dat")
set(top_srcdir "${CMAKE_CURRENT_SOURCE_DIR}")
string(REPLACE "/" "/\"\n     & //\"" FORTRAN_TESTS_DIR "${CMAKE_CURRENT_SOURCE_DIR}")
CONFIGURE_FILE(fopenfiles.h.in fopenfiles.h )
CONFIGURE_FILE(fthreadsafe.h.in fthreadsafe.h )

#####################################################################
# common options for test files
function(buildtestscommon execname)
  add_test( ${execname}  ${execname} )
  set_tests_properties(${execname} PROPERTIES ENVIRONMENT "srcdir=${CMAKE_CURRENT_SOURCE_DIR}")  
  if (WIN32)  
	set_property(TEST ${execname} PROPERTY ENVIRONMENT_MODIFICATION "PATH=path_list_append:${CMAKE_BINARY_DIR}/src")
  endif()
endfunction(buildtestscommon)

#####################################################################
# single C test file
function(buildtestscsimple execname sourcename)
  add_executable (${execname} ${sourcename})
  target_link_libraries (${execname} PRIVATE calcephtest calceph ${LIBM_LIBRARIES})
  buildtestscommon( ${execname} )
 endfunction(buildtestscsimple)

set (LIST_TEST_C_SIMPLE cversion csopenfail cmopenfail  csopen cmopen cmgetconstant csgetconstant cscheck cmcheck 
                 csgetconstantindex cmgetconstantindex
                 cmgetconstanttxtpck cmgetconstantindextxtpck cmcheckspk cmcomputeunitfail 
                 cmcomputeunit cmcomputeunit_naifid cmcheckspktt cmorientunitfail matrixfail 
                 tfmatrix cmcomputeunitfail2 checktpc_10086     
                 cmorientunitfailspk cmcomputeorder01 cmcomputeorder23 checkcst_11015 cmorientunitfail_11025 
                 crotangmomunitfail crotangmomunitfail2 crotangmomunit crotangmomorder0 crotangmomorder123 
                 cmtimescale cstimescale cmtimespan cstimespan cgetpositionrecordindex cgetorientrecordindex 
                 cmorientunitfail_11612 cmgetconstant_11627  cmopenfail_11628 cmgetconstantvd 
                 cmgetconstantvs csfileversionstr cmparallelcheck cmpolerade checktpc_12301 
                 cmaxsupportedderivative checktpc_12730 checktpc_incremental cmcomputeunit_framerelative
                 cmgetidbyname cmgetnamebyidss checktf_7
)
                 
foreach (C_SIMPLE IN LISTS LIST_TEST_C_SIMPLE)
    buildtestscsimple(${C_SIMPLE} ${C_SIMPLE}.c)
endforeach()



#####################################################################
# C test file with computehermite
function(buildtestschermite execname sourcename)
  add_executable (${execname} ${sourcename} cmcomputeunit_hermite.c)
  target_link_libraries (${execname} calcephtest calceph ${LIBM_LIBRARIES})
  buildtestscommon( ${execname} )
endfunction(buildtestschermite)

set (LIST_TEST_C_HERMITE cmcomputeunit_seg1 cmcomputeunit_seg8
                 cmcomputeunit_seg9 cmcomputeunit_seg12  cmcomputeunit_seg13 
                 cmcomputeunit_seg14 cmcomputeunit_seg21
                 cmcomputeunit_frame
)
                 
foreach (C_HERMITE IN LISTS LIST_TEST_C_HERMITE)
    buildtestschermite(${C_HERMITE} ${C_HERMITE}.c)
endforeach()

#####################################################################
# Fortran test file
if (ENABLE_FORTRAN)

    function(buildtestsfsimple execname sourcename)
      add_executable (${execname} ${sourcename})
      target_link_libraries (${execname} calcephtest calceph ${LIBM_LIBRARIES})
	  buildtestscommon( ${execname} )
    endfunction(buildtestsfsimple)

    set (LIST_TEST_FORTRAN_SIMPLE f2003sopenfail f2003mopenfail f2003sopen  f2003mopen f2003sgetconstant 
                     f2003mgetconstant f2003mcheck f2003sgetconstantindex f2003mgetconstantindex 
                     f2003mcomputeunit f2003mcomputeunit_naifid f2003version 
                     f2003mcomputeorder f2003rotangmomunit f2003rotangmomorder 
                     f2003mtimescale f2003mtimespan f2003stimescale f2003stimespan  
                     f2003getpositionrecordindex f2003getorientrecordindex 
                     f2003mgetconstantvd f2003mgetconstantvs f2003mfileversion f2003sfileversion 
                     f2003misthreadsafe f2003maxsupportedderivativeorder 
                     f2003mgetidbyname f2003mgetnamebyidss
                     f77sopenfail f77mopenfail f77sopen  f77mopen f77sgetconstant 
                     f77mgetconstant f77mcheck f77sgetconstantindex f77mgetconstantindex 
                     f77mcomputeunit  f77mcomputeunit_naifid f77version 
                     f77mcomputeorder f77rotangmomunit f77rotangmomorder 
                     f77mtimescale f77mtimespan f77stimescale f77stimespan  
                     f77getpositionrecordindex f77getorientrecordindex 
                     f77mgetconstantvd f77mgetconstantvs f77mfileversion f77sfileversion 
                     f77misthreadsafe f77maxsupportedderivativeorder
                     f77mgetidbyname f77mgetnamebyidss
    )
                 
    foreach( FORTRAN_SIMPLE IN LISTS LIST_TEST_FORTRAN_SIMPLE)
        buildtestsfsimple(${FORTRAN_SIMPLE} ${FORTRAN_SIMPLE}.f)
    endforeach()

endif()

set_property(TARGET cmcomputeorder23
        APPEND
        PROPERTY ADDITIONAL_MAKE_CLEAN_FILES example1_tests_23_derivative.dat
) 


#####################################################################
# C test file with extra files
function(buildtestsextra execname sourcename)
  add_executable (${execname} ${sourcename} cmcomputeunit_hermite.c)
  target_link_libraries (${execname} calcephtest calceph ${LIBM_LIBRARIES})
endfunction(buildtestsextra)

set (LIST_TEST_C_EXTRA  cmcomputeunit_seg5  cmcomputeunit_seg17 
                 cmcomputeunit_seg18 cmcomputeunit_seg20
)
                 
foreach (C_EXTRA IN LISTS LIST_TEST_C_EXTRA)
    buildtestsextra(${C_EXTRA} ${C_EXTRA}.c)
endforeach()
