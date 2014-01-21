!-------------------------------------------------------------------------------

!                      Code_Saturne version 2.1.0
!                      --------------------------
! This file is part of Code_Saturne, a general-purpose CFD tool.
!
! Copyright (C) 1998-2011 EDF S.A.
!
! This program is free software; you can redistribute it and/or modify it under
! the terms of the GNU General Public License as published by the Free Software
! Foundation; either version 2 of the License, or (at your option) any later
! version.
!
! This program is distributed in the hope that it will be useful, but WITHOUT
! ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
! FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
! details.
!
! You should have received a copy of the GNU General Public License along with
! this program; if not, write to the Free Software Foundation, Inc., 51 Franklin
! Street, Fifth Floor, Boston, MA 02110-1301, USA.

!-------------------------------------------------------------------------------

subroutine usalin
!================

!===============================================================================
!  Purpose :
! --------

! --- User subroutine dedicated to the use of ALE (Arbitrary Lagrangian Eulerian)
!     method :
!
!          Here one defines parameters and input data dedicated to the use ALE
!          method
!
!-------------------------------------------------------------------------------
! Arguments
!__________________.____._____.________________________________________________.
! name             !type!mode ! role                                           !
!__________________!____!_____!________________________________________________!
!__________________!____!_____!________________________________________________!

!     Type: i (integer), r (real), s (string), a (array), l (logical),
!           and composite types (ex: ra real array)
!     mode: <-- input, --> output, <-> modifies data, --- work array
!===============================================================================

!===============================================================================
! Module files
!===============================================================================

use paramx
use optcal
use albase

!===============================================================================

implicit none

! Arguments

! Local variables

!===============================================================================


!===============================================================================
!
!     Here are some examples that can be adapted and changed by Code Saturne
!     users.
!
!
!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_START
!ex
!ex ! --- Activation of ALE (Arbitrary Lagrangian Eulerian) method
!ex iale = 1
!ex
!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_END


!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_START
!ex
!ex ! --- Number of iterations for fluid initialization. Contrary to ntmabs (for example)
!ex !     nalinf is not an absolute iteration number, meaning that in case of
!ex !     restart calculation nalinf corresponds to the number of iterations
!ex !     for fuid initialization beginning from the first current iteration of
!ex !     the calculation restart. In general nalinf = 0 in that case.
!ex
!ex   nalinf = 75
!ex
!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_END

!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_START
!ex
!ex ! --- Maximum number of iterations in case of implicit Fluid Structure Coupling with structural
!ex !     calculations (internal and/or external(i.e. using Code_Aster)). NALIMX = 1, in case of
!ex !     explicit FSI algorithm.
!ex
!ex nalimx = 15
!ex
!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_END

!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_START
!ex
!ex ! --- Relative precision of sub-cycling Fluid Structure Coupling algorithm.
!ex epalim = 1.d-5
!ex
!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_END
!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_START
!ex
!ex ! --- Mesh viscosity modeling (cf. usvima)
!ex !     0 : isotropic
!ex !     1 : orthotropic
!ex iortvm = 0
!ex
!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_END

!----
! FORMATS
!----

!----
! End
!----

return
end subroutine
