%  /*-----------------------------------------------------------------*/
%  /*! 
%    \file CalcephBin.m
%    \brief MEX interface for the class Constants
%  
%    \author  M. Gastineau 
%             Astronomie et Systemes Dynamiques, IMCCE, CNRS, Observatoire de Paris. 
%  
%     Copyright,  2018-2024, CNRS
%     email of the author : Mickael.Gastineau@obspm.fr
%  
%    History:
%  */
%  /*-----------------------------------------------------------------*/
%  
%   /*-----------------------------------------------------------------*/
%   /* License  of this file :
%    This file is "triple-licensed", you have to choose one  of the three licenses 
%    below to apply on this file.
%    
%       CeCILL-C
%       	The CeCILL-C license is close to the GNU LGPL.
%       	( http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html )
%      
%    or CeCILL-B
%           The CeCILL-B license is close to the BSD.
%           (http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.txt)
%     
%    or CeCILL v2.1
%         The CeCILL license is compatible with the GNU GPL.
%         ( http://www.cecill.info/licences/Licence_CeCILL_V2.1-en.html )
%    
%   
%   This library is governed by the CeCILL-C, CeCILL-B or the CeCILL license under 
%   French law and abiding by the rules of distribution of free software.  
%   You can  use, modify and/ or redistribute the software under the terms 
%   of the CeCILL-C,CeCILL-B or CeCILL license as circulated by CEA, CNRS and INRIA  
%   at the following URL "http://www.cecill.info". 
%   
%   As a counterpart to the access to the source code and  rights to copy,
%   modify and redistribute granted by the license, users are provided only
%   with a limited warranty  and the software's author,  the holder of the
%   economic rights,  and the successive licensors  have only  limited
%   liability. 
%   
%   In this respect, the user's attention is drawn to the risks associated
%   with loading,  using,  modifying and/or developing or reproducing the
%   software by the user in light of its specific status of free software,
%   that may mean  that it is complicated to manipulate,  and  that  also
%   therefore means  that it is reserved for developers  and  experienced
%   professionals having in-depth computer knowledge. Users are therefore
%   encouraged to load and test the software's suitability as regards their
%   requirements in conditions enabling the security of their systems and/or 
%   data to be ensured and,  more generally, to use and operate it in the 
%   same conditions as regards security. 
%   
%   The fact that you are presently reading this means that you have had
%   knowledge of the CeCILL-C,CeCILL-B or CeCILL license and that you accept its terms.
%   */
%   /*-----------------------------------------------------------------*/

classdef CalcephBin < handle
%    A CalcephBin class to access the ephemeris file.

%    >>> import calceph
%    >>> f = calceph.open("ephemerisfile.dat")
%    >>> PV = f.compute(jd, dt, target, center)
%    >>> PV = peph.compute_unit(jd0, dt, NaifId.EARTH, NaifId.SUN, 
%                               Constants.UNIT_AU+Constants.UNIT_DAY+Constants.USE_NAIFID)
%    >>> f.close()
%    """
   properties (SetAccess = private, GetAccess = public)
   %% (Access = private, Hidden = true)
      c_handle
   end
      
   methods
        %% Constructor - Create a new Calceph class instance 
        function self = interfacemex()
            self.c_handle = 0;
        end
        
        %% Destructor - Destroy the Calceph class instance
        function delete(self)
            if self.c_handle~=0
                interfacemex('close', self.c_handle);
            end    
        end    

%/*-----------------------------------------------------------------*/
%/*-----------------------------------------------------------------*/
        function check_returnerror_null(self)
    %        """check if the ephemeris file is opened on exit and raise an exception"""
            % default initialization of the kind of error handler
            global usertypehandler_matlab
            if (isempty(usertypehandler_matlab))
                usertypehandler_matlab = 1;
            end
            if self.c_handle==0 && usertypehandler_matlab~=3
                error('No ephemeris files are opened');
            end
        end        

%/*-----------------------------------------------------------------*/
%/*-----------------------------------------------------------------*/
        function check_chandle_null(self)
%        """check if the ephemeris file is opened on input and raise an exception"""

            % default initialization of the kind of error handler
            global usertypehandler_matlab
            if (isempty(usertypehandler_matlab))
                usertypehandler_matlab = 1;
            end
            if self.c_handle==0 && usertypehandler_matlab~=3
                error('No ephemeris files are opened');
            end    
        end
        
%/*-----------------------------------------------------------------*/
%/*-----------------------------------------------------------------*/
        function self = close(self)
%   CLOSE  Close the ephemeris file.
            if self.c_handle~=0
                interfacemex('close', self.c_handle);
            end                   
            self.c_handle = 0;
        end
      
%/*-----------------------------------------------------------------*/
%/*-----------------------------------------------------------------*/
        function res = prefetch(self)
    %   PREFETCH Prefetch all data to memory
            self.check_returnerror_null();
            res = interfacemex('prefetch', self.c_handle);
            self.check_returnerror_0(res);
        end    

%/*-----------------------------------------------------------------*/
%/*-----------------------------------------------------------------*/
        function res = isthreadsafe(self)
    %   ISTHREADSAFE return non 0
            self.check_returnerror_null();
            res = interfacemex('isthreadsafe', self.c_handle);
        end    

%/*-----------------------------------------------------------------*/
%/*-----------------------------------------------------------------*/
        function PV = compute(self, JD0, time, target, center)
    %   COMPUTE Compute the position <x,y,z> and velocity <xdot,ydot,zdot>
    %           for a given target and center at a single time. The output is in UA, UA/day, radians
    %           
    %           return a list of 6 elements : position and the velocity of the "target" object.
    %    
    %           @param JD0 (in) reference time (could be 0)
    %           @param time (in) time ellapsed from JD0
    %           @param target (in) "target" object 
    %           @param center (in) "center" object
                                 
            self.check_chandle_null();
            [ res, PV ] = interfacemex('compute', self.c_handle, JD0, time, target, center);
            self.check_returnerror_0(res);
        end    


%/*-----------------------------------------------------------------*/
%/*-----------------------------------------------------------------*/
        function PV = compute_unit(self, JD0, time, target, center, unit)
          % COMPUTE_UNIT compute the position <x,y,z> and velocity <xdot,ydot,zdot>
          %  for a given target and center  at the specified time 
          %  (time ellapsed from JD0).
          %  The output is expressed according to unit.
          %
          %  return a list of 6 elements : position and the velocity of the "target" object.

          %  @param JD0 (in) reference time (could be 0)
          %  @param time (in) time ellapsed from JD0
          %  @param target (in) "target" object 
          %  @param center (in) "center" object 
          %  @param unit (in) sum of CALCEPH_UNIT_???
                                 
            self.check_chandle_null()
            [ res, PV ] = interfacemex('compute_unit', self.c_handle, JD0, time, target, center, unit);
            self.check_returnerror_0(res)
        end    

%/*-----------------------------------------------------------------*/
%/*-----------------------------------------------------------------*/
        function PV = orient_unit(self, JD0, time, target, unit)
            % orient_unit Return the orientation of the object "target"  at the specified time 
            % (time ellapsed from JD0).
            % The output is expressed according to unit.
            % 
            % return a list of 6 elements : orientation (euler angles and their derivatives) of the "target" object.
            %  
            % @param JD0 (in) reference time (could be 0)
            % @param time (in) time ellapsed from JD0
            % @param target (in) "target" object 
            % @param unit (in) sum of CALCEPH_UNIT_???
                                 
            self.check_chandle_null()
            [ res, PV ] = interfacemex('orient_unit', self.c_handle, JD0, time, target, unit);
            self.check_returnerror_0(res)
        end    

%/*-----------------------------------------------------------------*/
%/*-----------------------------------------------------------------*/
        function PV = rotangmom_unit(self, JD0, time, target, unit)
            % rotangmom_unit Return the rotional angular momentum (G/(mR^2)) of the object "target"  at the specified time 
            % (time ellapsed from JD0).
            % The output is expressed according to unit.
            % 
            %  return a list of 6 elements : rotional angular momentum  and their first derivatives of the "target" object.
            % 
            % @param JD0 (in) reference time (could be 0)
            % @param time (in) time ellapsed from JD0
            % @param target (in) "target" object 
            % @param unit (in) sum of CALCEPH_UNIT_???
                                 
            self.check_chandle_null()
            [ res, PV ] = interfacemex('rotangmom_unit', self.c_handle, JD0, time, target, unit);
            self.check_returnerror_0(res)
        end    

%/*-----------------------------------------------------------------*/
%/*-----------------------------------------------------------------*/
        function PV = compute_order(self, JD0, time, target, center, unit, order)
            % compute_order compute the position <x,y,z> and velocity <xdot,ydot,zdot>
            % for a given target and center  at the specified time
            % (time ellapsed from JD0).
            % The output is expressed according to unit.
            % 
            % return a list of 3*(order+1) floating-point numbers.
            % This list contains the positions and their deviatives of the "target" object
            % 
            % @param JD0 (in) reference time (could be 0)
            % @param time (in) time ellapsed from JD0
            % @param target (in) "target" object 
            % @param center (in) "center" object 
            % @param unit (in) sum of CALCEPH_UNIT_???
            % @param order (in) order of the computation
            % =0 : Positions are computed
            % =1 : Position+Velocity are computed
            % =2 : Position+Velocity+Acceleration are computed
            % =3 : Position+Velocity+Acceleration+Jerk are computed.
                                 
            self.check_chandle_null()
            [ res, PV ] = interfacemex('compute_order', self.c_handle, JD0, time, target, center, unit, order);
            self.check_returnerror_0(res)
        end    

%/*-----------------------------------------------------------------*/
%/*-----------------------------------------------------------------*/
        function PV = orient_order(self, JD0, time, target, unit, order)
            % orient_order Return the orientation of the object "target" at the specified time
            % (time ellapsed from JD0).
            % The output is expressed according to unit.
            % 
            % return a list of 3*(order+1) floating-point numbers.
            % This list contains the orientation (euler angles and their derivatives) of the "target" object
            % 
            % @param JD0 (in) reference time (could be 0)
            % @param time (in) time ellapsed from JD0
            % @param target (in) "target" object 
            % @param unit (in) sum of CALCEPH_UNIT_???
            % @param order (in) order of the computation
            %  =0 : orientations are computed
            %  =1 : orientations and their first derivatives are computed
            %  =2 : orientations and their first,second derivatives are computed
            %  =3 : orientations and their first, second, third derivatives are computed.
                                 
            self.check_chandle_null()
            [ res, PV ] = interfacemex('orient_order', self.c_handle, JD0, time, target, unit, order);
            self.check_returnerror_0(res)
        end    

%/*-----------------------------------------------------------------*/
%/*-----------------------------------------------------------------*/
        function PV = rotangmom_order(self, JD0, time, target, unit, order)
            % rotangmom_order Return the rotional angular momentum (G/(mR^2)) of the object "target" at the specified time
            % (time ellapsed from JD0).
            % The output is expressed according to unit.
            % 
            % return a list of 3*(order+1) floating-point numbers.
            % This list contains the rotional angular momentum (G/(mR^2)) and their derivatives of the "target" object
            % 
            % @param JD0 (in) reference time (could be 0)
            % @param time (in) time ellapsed from JD0
            % @param target (in) "target" object 
            % @param unit (in) sum of CALCEPH_UNIT_???
            % @param order (in) order of the computation
            %   =0 : (G/mR^2) are computed
            %   =1 : (G/mR^2) and their first derivatives are computed
            %   =2 : (G/mR^2) and their first,second derivatives  are computed
            %   =3 : (G/mR^2) and their first, second, third derivatives are computed.
                                 
            self.check_chandle_null()
            [ res, PV ] = interfacemex('rotangmom_order', self.c_handle, JD0, time, target, unit, order);
            self.check_returnerror_0(res)
        end    

%/*-----------------------------------------------------------------*/
%/*-----------------------------------------------------------------*/
        function val = getconstant(self, name)
            % getconstant get constant value from the specified name in the ephemeris file
            %
            %      name (in) name of the constant
            self.check_chandle_null()
            [ res, val ] = interfacemex('getconstant', self.c_handle, name);
            self.check_returnerror_0(res)
        end    

%/*-----------------------------------------------------------------*/
%/*-----------------------------------------------------------------*/
        function val = getconstantsd(self, name)
            % getconstantsd get constant value from the specified name in the ephemeris file
            %
            %      name (in) name of the constant
            self.check_chandle_null()
            [ res, val ] = interfacemex('getconstantsd', self.c_handle, name);
            self.check_returnerror_0(res)
        end    


%/*-----------------------------------------------------------------*/
%/*-----------------------------------------------------------------*/
        function val = getconstantvd(self, name)
            % getconstantvd get array of values from the specified name in the ephemeris file
            %
            %      name (in) name of the constant
            self.check_chandle_null()
            [ res, val ] = interfacemex('getconstantvd', self.c_handle, name);
            self.check_returnerror_0(res)
        end    

%/*-----------------------------------------------------------------*/
%/*-----------------------------------------------------------------*/
        function val = getconstantss(self, name)
            % getconstantss get constant value from the specified name in the ephemeris file
            %
            %      name (in) name of the constant
            self.check_chandle_null()
            [ res, val ] = interfacemex('getconstantss', self.c_handle, name);
            self.check_returnerror_0(res)
        end    


%/*-----------------------------------------------------------------*/
%/*-----------------------------------------------------------------*/
        function val = getconstantvs(self, name)
            % getconstantvs get array of values from the specified name in the ephemeris file
            %
            %      name (in) name of the constant
            self.check_chandle_null()
            [ res, val ] = interfacemex('getconstantvs', self.c_handle, name);
            self.check_returnerror_0(res)
        end    

%/*-----------------------------------------------------------------*/
%/*-----------------------------------------------------------------*/
        function val = getconstantcount(self)
        % getconstantcount Return the number of constants available in the ephemeris file
            self.check_chandle_null()
            val = interfacemex('getconstantcount', self.c_handle);
        end    


%/*-----------------------------------------------------------------*/
%/*-----------------------------------------------------------------*/
        function [ name, val ] = getconstantindex(self, index)
            % getconstantindex return the name and the associated value of the constant available at some index in the ephemeris file
            %   The value of index must be between 1 and getconstantcount().
            % 
            %      index (in) index of the constant. 
            self.check_chandle_null()
            [ res, name, val ] = interfacemex('getconstantindex', self.c_handle, index);
            self.check_returnerror_0(res)
        end    

% /*-----------------------------------------------------------------*/
% /*-----------------------------------------------------------------*/
        function [res, val] = getidbyname(self, name, unit) 
            % getidbyname get the id of the body from the specified name in the ephemeris file
            % 
            % name(in) name of the body 
            % unit(in) unit of the id 
            self.check_chandle_null()
            [res, val] = interfacemex('getidbyname', self.c_handle, name, unit);
        end

% /*-----------------------------------------------------------------*/
% /*-----------------------------------------------------------------*/
        function [res, name] = getnamebyidss(self, id, unit) 
            % getnamebyidss get the first given name of the body from the specified id in the ephemeris file
            % 
            % name(in) name of the body 
            % unit(in) unit of the id 
            self.check_chandle_null()
            [res, name] = interfacemex('getnamebyidss', self.c_handle, id, unit);
        end

%/*-----------------------------------------------------------------*/
%/*-----------------------------------------------------------------*/
        function val = getpositionrecordcount(self)
            % getpositionrecordcount return the number of position’s records available in the ephemeris file
            self.check_chandle_null()
            val = interfacemex('getpositionrecordcount', self.c_handle);
        end    


%/*-----------------------------------------------------------------*/
%/*-----------------------------------------------------------------*/
        function [ target, center, firsttime, lasttime, frame ] = getpositionrecordindex(self, index)
            % getpositionrecordindex return the target and origin bodies, the first and last time, and the reference frame available at the specified index for the position's records of the ephemeris file.
            %   The value of index must be between 1 and getpositionrecordcount().
            %
            %       index (in) index of the constant. 

            self.check_chandle_null()
            [ res, target, center, firsttime, lasttime, frame ] = interfacemex('getpositionrecordindex', self.c_handle, index);
            self.check_returnerror_0(res)
        end

%/*-----------------------------------------------------------------*/
%/*-----------------------------------------------------------------*/
        function [ target, center, firsttime, lasttime, frame, segid ] = getpositionrecordindex2(self, index)
            % getpositionrecordindex return the target and origin bodies, the first and last time, the reference frame and the semgent type available at the specified index for the position's records of the ephemeris file.
            %   The value of index must be between 1 and getpositionrecordcount().
            %
            %       index (in) index of the constant. 

            self.check_chandle_null()
            [ res, target, center, firsttime, lasttime, frame, segid ] = interfacemex('getpositionrecordindex2', self.c_handle, index);
            self.check_returnerror_0(res)
        end

%/*-----------------------------------------------------------------*/
%/*-----------------------------------------------------------------*/
        function val = getorientrecordcount(self)
            % getorientrecordcount return the number of orientation’s records available in the ephemeris file
            self.check_chandle_null()
            val = interfacemex('getorientrecordcount', self.c_handle);
        end    


%/*-----------------------------------------------------------------*/
%/*-----------------------------------------------------------------*/
        function [ target, firsttime, lasttime, frame ] = getorientrecordindex(self, index)
            % getorientrecordindex return the target and origin bodies, the first and last time, and the reference frame available at the specified index for the orientation's records of the ephemeris file.
            %   The value of index must be between 1 and getorientrecordcount().
            %
            %      index (in) index of the constant. 
        
            self.check_chandle_null()
            [ res, target, firsttime, lasttime, frame ] = interfacemex('getorientrecordindex', self.c_handle, index);
            self.check_returnerror_0(res)
        end

%/*-----------------------------------------------------------------*/
%/*-----------------------------------------------------------------*/
        function [ target, firsttime, lasttime, frame, segid ] = getorientrecordindex2(self, index)
            % getorientrecordindex return the target and origin bodies, the first and last time, the reference frame, and the segment type available at the specified index for the orientation's records of the ephemeris file.
            %   The value of index must be between 1 and getorientrecordcount().
            %
            %      index (in) index of the constant. 
        
            self.check_chandle_null()
            [ res, target, firsttime, lasttime, frame, segid ] = interfacemex('getorientrecordindex2', self.c_handle, index);
            self.check_returnerror_0(res)
        end

%/*-----------------------------------------------------------------*/
%/*-----------------------------------------------------------------*/
        function val = gettimescale(self)
            % gettimescale Return the time scale of the ephemeris file
            self.check_chandle_null()
            val = interfacemex('gettimescale', self.c_handle);
        end
        
%/*-----------------------------------------------------------------*/
%/*-----------------------------------------------------------------*/
        function [pfirsttime, plasttime, pcontinuous] = gettimespan(self)
            % Return the time span of the ephemeris file
            self.check_chandle_null()
            [res, pfirsttime, plasttime, pcontinuous] = interfacemex('gettimespan', self.c_handle);
            self.check_returnerror_0(res)
        end

%/*-----------------------------------------------------------------*/
%/*-----------------------------------------------------------------*/
        function val = getfileversion(self)
            % Return the file version of the ephemeris file
            self.check_chandle_null()
            [ res, val ] = interfacemex('getfileversion', self.c_handle);
        end    


    end

    
%/*-----------------------------------------------------------------*/
%/*-----------------------------------------------------------------*/
%/* --- static method ---*/
%/*-----------------------------------------------------------------*/
%/*-----------------------------------------------------------------*/
   methods (Static)
%/*-----------------------------------------------------------------*/
%/*-----------------------------------------------------------------*/
        function check_returnerror_0(res)
%        internal : check the error of the library  and raise an exception

            % default initialization of the kind of error handler
            global usertypehandler_matlab
            if (isempty('usertypehandler_matlab'))
                usertypehandler_matlab = 1;
            end
            if (res == 0) && (usertypehandler_matlab~=3)
                error('Calceph library has encountered a problem')
            end    
        end


%/*-----------------------------------------------------------------*/
%/*-----------------------------------------------------------------*/
        function r = open(pyarfilename)
%  OPEN  Open the file(s) pyarfilename
%    
%                  pyarfilename (in) a single string or an array of strings.
             r = CalcephBin(); %calceph.CalcephBin();
             r.c_handle = interfacemex('open', pyarfilename);
             r.check_returnerror_null()
        end

   end
   
end

               
