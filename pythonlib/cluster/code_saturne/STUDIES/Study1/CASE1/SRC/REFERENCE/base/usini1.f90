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

! Purpose:
! -------

! User subroutines for input of calculation parameters (Fortran commons).
!   These subroutines are called in all cases.

! If the Code_Saturne GUI is used, this file is not required (but may be
!   used to override parameters entered through the GUI, and to set
!   parameters not accessible through the GUI).

! Several routines are present in the file, each destined to defined
!   specific parameters.

! To modify the default value of parameters which do not appear in the
!   examples provided, code should be placed as follows:
!   - usipsu   for numerical and physical options
!   - usipes   for input-output related options

! As a convention, "specific physics" defers to the following modules only:
!   pulverized coal, gas combustion, electric arcs.

!-------------------------------------------------------------------------------


!===============================================================================


subroutine usipph &
!================

 ( iihmpu, nfecra , iturb , icp , iverif )


!===============================================================================
! Purpose:
! --------

! User subroutine for input of parameters depending on the number of phases.

!-------------------------------------------------------------------------------
! Arguments
!__________________.____._____.________________________________________________.
! name             !type!mode ! role                                           !
!__________________!____!_____!________________________________________________!
! iihmpu           ! i  ! <-- ! indicates if the XML file from the GUI is      !
!                  !    !     ! used (1: yes, 0: no)                           !
! nfecra           ! i  ! <-- ! Fortran unit number for standard output        !
! iturb            ! ia ! <-> ! turbulence model                               !
! icp              ! ia ! <-> ! flag for uniform Cp or not                     !
! iverif           ! i  ! <-- ! flag for elementary tests                      !
!__________________!____!_____!________________________________________________!

!     Type: i (integer), r (real), s (string), a (array), l (logical),
!           and composite types (ex: ra real array)
!     mode: <-- input, --> output, <-> modifies data, --- work array
!===============================================================================

!===============================================================================
! Module files
!===============================================================================

! No module should appear here


!===============================================================================

implicit none

! Arguments

integer iihmpu, nfecra
integer iturb, icp
integer iverif

! Local variables

!===============================================================================


!===============================================================================


!     In this subroutine, only the parameters which already appear may

!       be set, to the exclusion of any other.
!               ================


!     If we are not using the Code_Saturne GUI:

!       All the parameters which appear in this subroutine must be set.
!       ===


!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_START
!ex
!ex !     If we are using the Code_Saturne GUI:
!ex
!ex !       we will find in the user subroutines commented examples
!ex !       on the model of the present section.
!ex
!ex !       If necessary, the user may uncomment them and adapt them to
!ex !       his needs.
!ex
!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_END

!===============================================================================

! --- Turbulence (for each phase)
!       0...Laminar
!      10...Mixing length
!      20...k-epsilon
!      21...k-epsilon (linear production)
!      30...Rij-epsilon, (standard LRR)
!      31...Rij-epsilon (SSG)
!      40...LES (Smagorinsky)
!      41...LES (Dynamic)
!      42...LES (WALE)
!      50...v2f (phi-model)
!      51...v2f (BL-v2/k)
!      60...k-omega SST
!      70...Spalart Allmaras
!  For 10, contact the development team before use

!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_START
!ex
!ex iturb = 20
!ex
!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_END


! --- Variable specific heat (ICP=1) or not (ICP=0)

!     Should be set only if specific physics (coal, combustion, electric arcs)
!       ARE NOT activated.

!     For these specific physics, ICP MUST NOT BE MODIFIED here, and the
!       following options are forced:
!          coal and combustion: constant CP constant;
!          electric arcs:       variable CP.

!     Caution:    complete usphyv with the law defining Cp
!     =========   if and only if variable Cp has been selected here
!                 (with icp=1)

!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_START
!ex
!ex icp = 0
!ex
!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_END

!----
! Formats
!----


return
end subroutine


!===============================================================================


subroutine usinsc &
!================

 ( iihmpu, nfecra , nscaus , iverif )


!===============================================================================
! Purpose:
! -------

! User subroutine for input of the number of user scalars.

!-------------------------------------------------------------------------------
! Arguments
!__________________.____._____.________________________________________________.
! name             !type!mode ! role                                           !
!__________________!____!_____!________________________________________________!
! iihmpu           ! i  ! <-- ! indicates if the XML file from the GUI is      !
!                  !    !     ! used (1: yes, 0: no)                           !
! nfecra           ! i  ! <-- ! Fortran unit number for standard output        !
! nscaus           ! i  ! <-> ! number of user scalars                         !
! iverif           ! i  ! <-- ! flag for elementary tests                      !
!__________________!____!_____!________________________________________________!

!     Type: i (integer), r (real), s (string), a (array), l (logical),
!           and composite types (ex: ra real array)
!     mode: <-- input, --> output, <-> modifies data, --- work array
!===============================================================================

!===============================================================================
! Module files
!===============================================================================


! No module should appear here


!===============================================================================

implicit none

! Arguments

integer iihmpu, nfecra
integer nscaus
integer iverif

! Local variables


!===============================================================================


!===============================================================================


!     In this subroutine, only the parameters which already appear may

!       be set, to the exclusion of any other.
!               ================


!     If we are not using the Code_Saturne GUI:

!       All the parameters which appear in this subroutine must be set.
!       ===


!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_START
!ex
!ex !     If we are using the Code_Saturne GUI:
!ex
!ex !       we will find in the user subroutines commented examples
!ex !       on the model of the present section.
!ex
!ex !       If necessary, the user may uncomment them and adapt them to
!ex !       his needs.
!ex
!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_END

!===============================================================================

! --- Number of USER scalars (thermal or not, and whatever their carrier phase).
!       These scalars come in addition to the following "basic" scalars
!       (which are naturally included in the model):
!        - pressure
!        - turbulent variables
!        - nscapp scalars introduced by an active combustion, coal,
!          or electric arc module.

!     Thus, for a calculation with no specific physics, the user scalars
!       may for example be:
!        - temperature or enthalpy,
!        - mass fractions of transported scalars
!        - the variance of another user scalar

!     The maximum number of scalars is defined by 'nscamx' in paramx.h;
!       it is the maximum admissible value for: nscaus + nscapp.


!     Set nscaus = 0 if there is no user scalar.

!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_START
!ex
!ex nscaus = 0
!ex
!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_END

!----
! Formats
!----


return
end subroutine


!===============================================================================


subroutine usipsc &
!================

 ( nscmax, nscaus, iihmpu, nfecra, iscavr, ivisls , iverif )


!===============================================================================
! Purpose:
! -------

! User subroutine for the input of parameters depending on the
!   number of user scalars.

!-------------------------------------------------------------------------------
! Arguments
!__________________.____._____.________________________________________________.
! name             !type!mode ! role                                           !
!__________________!____!_____!________________________________________________!
! nscmax           ! i  ! <-- ! maximum number of scalars                      !
! nscaus           ! i  ! <-- ! number of user scalars                         !
! iihmpu           ! i  ! <-- ! indicates if the XML file from the GUI is      !
!                  !    !     ! used (1: yes, 0: no)                           !
! nfecra           ! i  ! <-- ! Fortran unit number for standard output        !
! iscavr(nscmax)   ! ia ! <-- ! associated scalar number for variance scalars  !
! ivisls(nscmax)   ! ia ! <-> ! uniform scalar diffusivity flag                !
! iverif           ! i  ! <-- ! flag for elementary tests                      !
!__________________!____!_____!________________________________________________!

!     Type: i (integer), r (real), s (string), a (array), l (logical),
!           and composite types (ex: ra real array)
!     mode: <-- input, --> output, <-> modifies data, --- work array
!===============================================================================

!===============================================================================
! Module files
!===============================================================================


! No module should appear here


!===============================================================================

implicit none

! Arguments

integer nscmax, nscaus, iihmpu, nfecra
integer iscavr(nscmax), ivisls(nscmax)
integer iverif

! Local variables

integer iutile, iscal

!===============================================================================


!===============================================================================


!     In this subroutine, only the parameters which already appear may

!       be set, to the exclusion of any other.
!               ================


!     If we are not using the Code_Saturne GUI:

!       All the parameters which appear in this subroutine must be set.
!       ===


!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_START
!ex
!ex !     If we are using the Code_Saturne GUI:
!ex
!ex !       we will find in the user subroutines commented examples
!ex !       on the model of the present section.
!ex
!ex !       If necessary, the user may uncomment them and adapt them to
!ex !       his needs.
!ex
!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_END

!===============================================================================

! --- Variance of a USER scalar:
!     If we wish a user scalar j to represent the variance of a
!       user scalar k, we set
!       iscavr(j) = k.
!     The values taken by iscavr are thus naturally greater or equal to 1
!       and less than or equal to the total number of scalars.
!       So, if we set iscavr(j) = k, we must have
!       0 < j < nscaus+1, 0< k < nscaus+1 and j different from k.

!     For example for user scalar 3 to be the variance of user scalar 2,
!       we set:
!       iscavr(3) = 2
!       with nscaus at least equal to 3.

!     Do not intervene if you do not wish to explicitly include the
!       variance of a user scalar in the simulation.

!     For non-user scalars relative to specific physics (coal, combustion,
!       electric arcs: see usppmo) implicitly defined in the model,
!       the corresponding information is given automatically, and
!       iscavr should not be modified.


!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_START
!ex
!ex !     The test on iutile allows deactivation of the instructions
!ex !       (which are only given as an example).
!ex
!ex iutile = 0
!ex if (iutile.eq.1) then
!ex   iscavr(3) = 2
!ex endif
!ex
!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_END




! --- Variable diffusivity (ivisls=1) or constant diffusivity (ivisls=0) for
!       each USER scalar, EXCEPT those which represent the variance
!       of another.

!     For user scalars iscal which represent the variance of another user
!       scalar, we do not set ivisls(iscal) here.
!       This is the purpose of the test on iscavr(ISCAL) in the example below.
!       Indeed, the diffusivity of the variance of a scalar is assumed to
!       have the same behavior as the diffusivity of this scalar.

!     For non-user scalars relative to specific physics (coal, combustion,
!       electric arcs: see usppmo) implicitly defined in the model,
!       the corresponding information is given automatically, and
!       ivisls should not be modified here.

!     Caution:    complete usphyv with the law defining the diffusivity
!     =========   if and only if ivisls = 1 has been set here.



!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_START
!ex
!ex do iscal = 1, nscaus
!ex
!ex   ! For user scalars which do not represent the variance of another scalar
!ex   if (iscavr(iscal).le.0) then
!ex
!ex     ivisls(iscal) = 0
!ex
!ex   endif
!ex
!ex enddo
!ex
!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_END

!----
! Formats
!----



return
end subroutine


!===============================================================================


subroutine usipgl &
!================

 ( nesmax,                                                        &
   iespre, iesder, iescor, iestot,                                &
   iihmpu, nfecra,                                                &
   idtvar, ipucou, iphydr, ialgce , iescal , iverif ,             &
   icwfps, cwfthr )


!===============================================================================
! Purpose:
! -------

! User subroutine for the setting of global parameters.

!-------------------------------------------------------------------------------
! Arguments
!__________________.____._____.________________________________________________.
! name             !type!mode ! role                                           !
!__________________!____!_____!________________________________________________!
! nesmax           ! i  ! <-- ! maximum number of error estimators per phase   !
! iespre           ! i  ! <-- ! number of the prediction error estimator       !
! iesder           ! i  ! <-- ! number of the derivative error estimator       !
! iescor           ! i  ! <-- ! number of the correction error estimator       !
! iestot           ! i  ! <-- ! number of the total error estimator            !
! iihmpu           ! i  ! <-- ! indicates if the XML file from the GUI is      !
!                  !    !     ! used (1: yes, 0: no)                           !
! nfecra           ! i  ! <-- ! Fortran unit number for standard output        !
! idtvar           ! i  ! --> ! variable time step flag                        !
! ipucou           ! i  ! --> ! reinforced u-p coupling flag                   !
! iphydr           ! i  ! --> ! flag for handling of the equilibrium between   !
!                  !    !     ! the pressure gradient and the gravity and      !
!                  !    !     ! head-loss terms                                !
! ialgce           ! i  ! <-- ! option for the method of calculation of        !
!                  !    !     !  cell centers                                  !
! iescal(nesmax)   ! ia ! <-- ! flag for activation of error estimators for    !
!                  !    !     ! Navier-Stokes                                  !
! iverif           ! i  ! <-- ! flag for elementary tests                      !
! cwfthr           ! i  ! <-- ! Treshold angle to cut warped faces (do not     !
!                  !    !     !  cut warped faces if value is negative)        !
!__________________!____!_____!________________________________________________!

!     Type: i (integer), r (real), s (string), a (array), l (logical),
!           and composite types (ex: ra real array)
!     mode: <-- input, --> output, <-> modifies data, --- work array
!===============================================================================

!===============================================================================
! Module files
!===============================================================================


! No module should appear here


!===============================================================================

implicit none

! Arguments

integer nesmax
integer iespre, iesder, iescor, iestot
integer iihmpu, nfecra
integer idtvar, ipucou, iphydr, ialgce
integer iescal(nesmax)
integer iverif, icwfps

double precision cwfthr

! Local variables

!===============================================================================


!===============================================================================


!     In this subroutine, only the parameters which already appear may

!       be set, to the exclusion of any other.
!               ================


!     If we are not using the Code_Saturne GUI:

!       All the parameters which appear in this subroutine must be set.
!       ===


!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_START
!ex
!ex !     If we are using the Code_Saturne GUI:
!ex
!ex !       we will find in the user subroutines commented examples
!ex !       on the model of the present section.
!ex
!ex !       If necessary, the user may uncomment them and adapt them to
!ex !       his needs.
!ex
!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_END

!===============================================================================

! --- Time step  (0 : uniform and constant
!                 1 : variable in time, uniform in space
!                 2 : variable in time and space
!                -1 : steady algorithm)

!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_START
!ex
!ex idtvar = 0
!ex
!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_END


! --- Velocity/pressure coupling (0 : classical algorithm,
!                                 1 : transient coupling)
!     Only in single-phase

!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_START
!ex
!ex ipucou = 0
!ex
!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_END


! --- Handling of hydrostatic pressure
!                               (0 : usual algorithm
!                                1 : specific handling)
!     Only in single-phase

!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_START
!ex
!ex iphydr = 0
!ex
!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_END


! --- Estimators for Navier-Stokes (non-frozen velocity field)
!     We recommend running a calculation restart on a few time steps
!       with the activation of the most interesting of those.
!        (=2 to activate, =0 to deactivate).

!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_START
!ex
!ex !       div(rho u) -Gamma
!ex iescal(iescor) = 0
!ex !       resolution precision for the momentum
!ex iescal(iestot) = 0
!ex
!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_END


! --- Triangulate warped faces:
!       If cwfthr is positive, faces whose warping angle are greater than
!         the given value (in degrees) are subdivided into triangles;
!       if cwfthr negative, faces are not subdivided.
!       If icwfps = 1, additional postprocessing will be activated to
!         show faces before and after cutting.

!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_START
!ex
!ex icwfps = 0
!ex cwfthr= -1.d0
!ex
!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_END


!----
! Formats
!----


return
end subroutine


!===============================================================================


subroutine usipsu &
!================

 ( nmodpp , iverif )


!===============================================================================
! Purpose:
! -------

! User subroutine for the input of additional user parameters.

!-------------------------------------------------------------------------------
! Arguments
!__________________.____._____.________________________________________________.
! name             !type!mode ! role                                           !
!__________________!____!_____!________________________________________________!
! nmodpp           ! i  ! <-- ! number of active specific physics models       !
! iverif           ! i  ! <-- ! flag for elementary tests                      !
!__________________!____!_____!________________________________________________!

!     Type: i (integer), r (real), s (string), a (array), l (logical),
!           and composite types (ex: ra real array)
!     mode: <-- input, --> output, <-> modifies data, --- work array
!===============================================================================

!===============================================================================
! Module files
!===============================================================================

use paramx
use cstnum
use dimens
use numvar
use optcal
use cstphy
use entsor
use mltgrd
use parall
use period
use ihmpre
use ppppar
use ppthch
use ppincl
use coincl
use cpincl
use elincl

!===============================================================================

implicit none

! Arguments

integer nmodpp
integer iverif

! Local variables

integer iutile, ii, jj, imom

!===============================================================================


!===============================================================================


!     This subroutine allows setting parameters

!       which do not already appear in the other subroutines of this file.


!     It is possible to add or remove parameters.


!     The number of physical properties and variables is known here.


!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_START
!ex
!ex !     If we are using the Code_Saturne GUI:
!ex
!ex !       we will find in the user subroutines commented examples
!ex !       on the model of the present section.
!ex
!ex !       If necessary, the user may uncomment them and adapt them to
!ex !       his needs.
!ex
!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_END

!===============================================================================


! Calculation options (optcal.h)
! ==============================

!     In case of restart, read auxiliary restart file ileaux (= 1) or not (0).

!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_START
!ex
!ex ileaux = 1
!ex
!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_END

! --- Duration
!       ntmabs = absolute number of the last time step required
!         if we have already run 10 time steps and want to
!         run 10 more, ntmabs must be set to 10 + 10 = 20

!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_START
!ex
!ex ntmabs = 10
!ex
!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_END

! --- Reference time step
!     The example given below is probably not adapted to your case.

!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_START
!ex
!ex dtref  = 0.01d0
!ex
!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_END

! --- Maximum time step: dtmax
!     Set a value base on characteristic values of your case.
!      otherwise, the code will use a multiple of dtref by default.
!     Example with
!        Ld: "dynamic" length (for example, the domain length)
!        Ud: characteristic flow velocity
!        Lt: thermal length (for example, the domain height gravity-wise)
!        Delta_rho/rho: relative density difference
!        g: gravity acceleration

!     dtmax = min(Ld/Ud, sqrt(Lt/(g.Delta_rho/rho)))



! --- Temperature or enthalpy



!   When specific physics are activated (coal, combustion, electric arcs)
!     we DO NOT edit this section: we DO NOT modify 'iscalt' nor 'iscsth'
!    (the test: if (nmodpp.eq.0) is used for this).


!   On the other hand, if specific physics are NOT activated:

!     If a USER scalar represents the temperature or enthalpy:
!       we define the number of this scalar in iscalt and
!       we set iscsth(iscalt) = 1 if it is the temperature
!          or  iscsth(iscalt) = 2 if it is the enthalpy.

!     If no scalar represents the temperature or enthalpy
!       we set iscalt = -1
!       and we do not define iscsth(iscalt).


!     For the radiative module when used without specific physics, if we
!      have chosen to solve in temperature (that is if
!      iscsth(iscalt) = 1), the fluid temperature is considered to
!      be in degrees KELVIN (be careful for boundary conditions an expression
!      of physical properties depending on temperature).
!      Nonetheless, even though it is not recommended, if we wish for the
!      fluid solver to work with a temperature in degrees Celsius, we must set
!      iscsth(iscalt) = -1.
!      This choice is a source of user errors. Indeed, the boundary conditions
!      for the fluid temperature will then be in degrees Celsius, while the
!      boundary conditions for radiation in usray2 must still be in Kelvin.


!    If specific physics are not activated
!       (coal, combustion, electric arcs: see usppmo):

!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_START
!ex
!ex if (nmodpp.eq.0) then
!ex
!ex   ! Number of the scalar representing temperature or enthalpy,
!ex   !   or -1 if there is none.
!ex   ! When the choice is done by the Code_Saturne GUI, the scalar representing
!ex   !   the temperature or enthalpy is always the first.
!ex   iscalt = -1
!ex
!ex ! If there is a temperature or enthalpy variable:
!ex   if (iscalt.gt.0) then
!ex     ! we indicate if it is the temperature (=1) or the enthalpy (=2).
!ex     iscsth(iscalt) = 1
!ex   endif
!ex
!ex endif
!ex
!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_END

! --- Calculation (restart) with frozen velocity field (1 yes, 0 no)

!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_START
!ex
!ex iccvfg = 0
!ex
!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_END

! --- Vortex method for inlet conditions in L.E.S.
!       (0: not activated,  1: activated)
!     The vortex method only regards the L.E.S. models
!       and is only valid with one phase.
!     To use the vortex method, edit the 'usvort.f90' user file.

!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_START
!ex
!ex if (itytur.eq.4) then
!ex   ivrtex = 0
!ex endif
!ex
!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_END

! --- Convective scheme

!     blencv = 0 for upwind (order 1 in space, "stable but diffusive")
!            = 1 for centered/second order (order 2 in space)
!       we may use intermediate real values.
!       Here we choose:
!         for the velocity of phase 1 and user scalars:
!           an upwind-centered scheme with 100% centering (blencv=1)
!         for other variables
!           the default code value (upwind standard, centered in LES)

!     Specifically, for user scalars
!       if we suspect an excessive level of numerical diffusion on
!         a variable ivar representing a user scalar
!         iscal (with ivar=isca(iscal)), it may be useful to set
!         blencv(ivar) = 1.0d0 to use a second-order scheme in space for
!         convection. For temperature or enthalpy in particular, we
!         may thus choose in this case:
!          blencv(isca(iscalt)) = 1.0d0

!       For non-user scalars relative to specific physics (coal, combustion,
!         electric arcs: see usppmo) implicitly defined by the model,
!         the corresponding information is set automatically elsewhere:
!         we do not modify blencv here.


!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_START
!ex
!ex blencv(iu) = 1.0d0
!ex blencv(iv) = 1.0d0
!ex blencv(iw) = 1.0d0
!ex if (nscaus.ge.1) then
!ex   do ii = 1, nscaus
!ex     blencv(isca(ii)) = 1.0d0
!ex   enddo
!ex endif
!ex
!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_END


! --- Linear solver parameters (for each unknown)

!     iresol = -1:           default
!     iresol = 1000*ipol +j: ipol is the degree of the Neumann polynomial
!                            used for preconditioning,
!                            j = 0: conjugate gradient,
!                            j = 1: Jacobi
!                            j = 2: bi-CgStab
!                            j = 3: GMRES

!     nitmax: maximum number of iterations for each unknown ivar
!     epsilo: relative precision for the solution of the linear system.

!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_START
!ex
!ex iutile = 0
!ex if (iutile.eq.1) then
!ex
!ex   iresol(iu) = 2
!ex   iresol(iv) = 2
!ex   iresol(iw) = 2
!ex   if (nscaus.ge.1) then
!ex     do ii = 1, nscaus
!ex       iresol(isca(ii)) = 2
!ex       nitmax(isca(ii)) = 5000
!ex       epsilo(isca(ii)) = 1.d-6
!ex     enddo
!ex   endif
!ex
!ex endif
!ex
!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_END


! --- Algebraic multigrid parameters

!     imgr = 0: no multigrid
!     imgr = 1: algebraic multigrid

!     Only available for pressure and purely diffusive variables.

!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_START
!ex
!ex ! mltmmn = 300  ! mean number of cells under which merging takes place
!ex ! mltmgl = 500  ! global number of cells under which merging takes place
!ex ! mltmmr = 1    ! number of active ranks under which no merging is done
!ex ! mltmst = 4    ! number of ranks over which merging takes place
!ex
!ex imgr(ipr) = 1
!ex
!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_END


!=========================================================================

! --- Stabilization in turbulent regime

!     For difficult cases, a stabilization may be obtained by not
!     reconstructing the convective and diffusive flux for variables
!     of the turbulence model, that is
!       in k-epsilon: if (itytur.eq.2) then
!          ircflu(ik)   = 0 and ircflu(iep)  = 0
!       in Rij-epsilon: if (itytur.eq.3) then
!          ircflu(ir11) = 0,    ircflu(ir22) = 0,
!          ircflu(ir33) = 0,
!          ircflu(ir12) = 0,    ircflu(ir23) = 0,
!          ircflu(ir23) = 0,
!                                  and ircflu(iep)  = 0
!     (note that variable itytur is equal to iturb/10)

!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_START
!ex
!ex !     The test on iutile allows deactivation of the instructions
!ex !       (which are only given as an example).
!ex
!ex iutile = 0
!ex if (iutile.eq.1) then
!ex
!ex   if (iturb.eq.20) then
!ex     ircflu(ik)   = 0
!ex     ircflu(iep)  = 0
!ex   endif
!ex
!ex endif
!ex
!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_END


! Physical constants (cstphy.h)
! =============================

! --- gravity (g in m/s2, with the sign in the calculation coordinate axes).

!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_START
!ex
!ex gx = 0.d0
!ex gy = 0.d0
!ex gz = 0.d0
!ex
!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_END

! --- rotation vector of the reference frame (omega in s-1)

!       If the rotation is not nul, then
!          icorio = 0: rotation is taken into account by rotating the mesh
!                      (simulation in the absolute frame)
!                 = 1: rotation is taken into account by Coriolis source terms
!                      (simulation in the relative frame)

!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_START
!ex
!ex icorio = 0
!ex
!ex omegax = 0.d0
!ex omegay = 0.d0
!ex omegaz = 0.d0
!ex
!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_END

! --- Reference fluid properties (for each phase)

!       ro0        : density in kg/m3
!       viscl0     : dynamic viscosity in kg/(m s)
!       cp0        : specific heat in J/(degres kg)
!       t0         : reference temperature in Kelvin
!       p0         : total reference pressure in Pascal
!                    the calculation is based on a
!                    reduced pressure P*=Ptot-ro0*g.(x-xref)
!                    (except in compressible case)
!       xyzp0(3)   : coordinates of the reference point for
!                    the total pressure (where it is equal to p0)

!     In general, it is not necessary to furnish a reference point xyz0.
!       If there are outlets, the code will take the center of the
!       reference outlet face.
!       On the other hand, if we plan to explicitly fix Dirichlet conditions
!       for pressure, it is better to indicate to which reference the
!       values relate (for a better resolution of reduced pressure).


!     Other properties are given by default in all cases.

!     Nonetheless, we may note that:

!       In the standard case (no gas combustion, coal, electric arcs,
!                             compressibility):
!       ---------------------
!         ro0, viscl0 and cp0
!             are useful and represent either the fluid properties if they
!             are constant, either simple mean values for the initialization
!             if properties are variable and defined in usphyv.
!         t0  is not useful
!         p0  is useful but is not used in an equation of state. p0
!             is a reference value for the incompressible solver
!             which will serve to set the (possible) domain outlet pressure.
!             We may also take it as 0 or as a physical value in Pascals.

!       With the electric module:
!       ------------------------
!         ro0, viscl0 and cp0
!             are useful but simply represent mean initial values;
!             the density, molecular dynamic viscosity, and specific
!             heat are necessarily given in propce (whether they are
!             physically variable or not): see uselph for the Joule effect
!             module and the electric arcs dp_ELE data file.
!         t0  is useful an must be in Kelvin (> 0) but represents a simple
!             initialization value.
!         p0  is useful bu is not used in the equation of state. p0
!             is a reference value for the incompressible solver which
!             will be used to calibrate the (possible) outlet pressure
!             of the domain. We may take it as zero or as a physical
!             value in Pascals.

!       With gas combustion:
!       --------------------
!         ro0 is not useful (it is automatically recalculated by the
!             law of ideal gases from t0 and p0).
!         viscl0 is indispensable: it is the molecular dynamic viscosity,
!             assumed constant for the fluid.
!         cp0 is indispensable: it is the heat capacity, assumed constant,
!             (modelization of source terms involving a local Nusselt in
!             the Lagrangian module, reference value allowing the
!             calculation of a radiative
!             (temperature, exchange coefficient) couple).
!         t0  is indispensible and must be in Kelvin (> 0).
!         p0  is indispensable and must be in Pascal (> 0).

!       With pulverized coal:
!       ---------------------
!         ro0 is not useful (it is automatically recalculated by the
!             law of ideal gases from t0 and p0).
!         viscl0 is indispensable: it is the molecular dynamic viscosity,
!             assumed constant for the fluid (its effect is expected to
!             be small compared to turbulent effects).
!         cp0 is indispensable: it is the heat capacity, assumed constant,
!             (modelization of source terms involving a local Nusselt in
!             the coal or Lagrangian module, reference value allowing the
!             calculation of a radiative
!             (temperature, exchange coefficient) couple).
!         t0  is indispensable and must be in Kelvin (> 0).
!         p0  is indispensable and must be in Pascal (> 0).

!       With compressibility:
!       ---------------------
!         ro0 is not useful, stricto sensu; nonetheless, as experience
!             shows that users often use this variable, it is required
!             to assign to it a strictly positive value (for example,
!             an initial value).
!         viscl0 is useful and represents the molecular dynamic viscosity,
!             when it is constant, or a value which will be used during
!             initializations (or in inlet turbulence conditions,
!             depending on the user choice.
!         cp0 is indispensable: it is the heat capacity, assumed constant
!             in the thermodynamics available by default
!         t0  is indispensable and must be in Kelvin (> 0).
!         p0  is indispensable and must be in Pascal (> 0).
!             With the thermodynamic law available by default,
!             t0 and p0 are used for the initialization of the density.
!         xyzp0 is not useful because the pressure variable directly
!             represents the total pressure.


!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_START
!ex
!ex ro0    = 0.235d0
!ex viscl0 = 0.84d-6
!ex cp0    = 1219.d0
!ex
!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_END

t0 = 1000.d0 + 273.15d0
p0 = 1.01325d5
! We only specify XYZ0 if we explicitely fix Dirichlet conditions
! for the pressure.
! xyzp0(1) = 0.d0
! xyzp0(2) = 0.d0
! xyzp0(3) = 0.d0


! --- irovar, ivivar: density and viscosity constant or not ?

!     When a specific physics module is active
!       (coal, combustion, electric arcs, compressible: see usppmo)
!       we DO NOT set variables 'irovar' and 'ivivar' here, as
!       they are defined automatically.
!     Nonetheless, for the compressible case, ivivar may be modified
!       in the uscfx1 user subroutine.

!     When no specific physics module is active, it is necessary to
!       specify if the density and the molecular viscosity
!         are constant (irovar=0, ivivar=0)
!          or variable (irovar=1, ivivar=1)

!       if they are variable, the law must be defined in usphyv;
!       if they are constant, they take values ro0 and viscl0.

!       as an example, we assume below that they are constant.

!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_START
!ex
!ex if (nmodpp.eq.0) then
!ex   irovar = 0
!ex   ivivar = 0
!ex endif
!ex
!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_END


! --- Minimum (scamin) and maximum (scamax) admissible values for
!        each USER scalar:

!      Results are clipped at the end of each time step.

!      If scamin > scamax, we do not clip.

!      For a scalar jj representing the variance of another, we may
!        abstain from defining these values
!        (a default clipping is set in place).
!        This is the purpose of the test on iscavr(jj) in the example below.

!      For non-user scalars relative to specific physics (coal, combustion,
!        electric arcs: see usppmo) implicitly defined according to the
!        model, the information is automatically set elsewhere: we
!        do not set scamin or scamax.

!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_START
!ex
!ex ! If there are user scalars
!ex if (nscaus.gt.0) then
!ex
!ex   ! Loop on user scalars:
!ex   do jj = 1, nscaus
!ex     ! For scalars which are not variances
!ex     if (iscavr(jj).le.0) then
!ex       ! We define the min and max bounds
!ex       scamin(jj) =-grand
!ex       scamax(jj) =+grand
!ex     endif
!ex   enddo
!ex
!ex endif
!ex
!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_END

! --- Reference diffusivity visls0 in kg/(m s) for each
!        USER scalar except those which represent the variance of another.

!     For non-user scalars relative to specific physics (coal, combustion,
!       electric arcs: see usppmo) implicitly defined in the model,
!       the information is given automatically elsewhere:
!       we do not modify visls0 here.

!     For user scalars JJ which represent the variance of another user
!       scalar, we do not define visls0(jj) here.
!       This is the purpose of the test on iscavr(jj) in the example below.
!       Indeed the diffusivity of the variance of a scalar is assumed
!       identical to that scalar's diffusivity.

!     When no specific physics has been activated
!       (coal, combustion, electric arcs) and if a user scalar represents
!       the temperature or enthalpy:
!       visls0(iscalt) = Lambda/Cp

!     Here, as an example, we assign to viscl0 the viscosity of the
!       carrier phase, which is fitting for passive tracers which
!       follow the fluid.


!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_START
!ex
!ex ! If there are user scalars
!ex if (nscaus.gt.0) then
!ex
!ex   ! We loop on user scalars:
!ex   do jj = 1, nscaus
!ex     ! For scalars which are not variances
!ex     if (iscavr(jj).le.0) then
!ex       ! We define the diffusivity
!ex       visls0(jj) = viscl0
!ex     endif
!ex   enddo
!ex
!ex endif
!ex
!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_END


! --- Reference velocity for turbulence initialization (m2/s)
!       (useful only with turbulence)

!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_START
!ex
!ex uref    = 1.d0
!ex
!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_END

! --- Reference length scale in meters for initialization
!       of epsilon (and specific clipping of turbulence, but
!       this is not the default option)
!       Assign a value of the order of the largest dimension of the
!       physical domain in which the flow may develop.
!       (useful only for turbulence).

!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_START
!ex
!ex almax = -grand
!ex
!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_END

! --- Definition of moments
!     (at the most nbmomx moments, correlations of maximum order ndgmox)

!     We calculate temporal means of the type <f1*f2*f3*...*fn>
!     The fi's are cell-defined variables (arrays rtp and propce).

!        idfmom(i,imom) ientifies the variable fi of moment imom
!          if idfmom > 0 it is a resolved variable (rtp)
!          if idfmom < 0 it is an auxiliary variable (propce)
!        imoold(imom) defined in the case of a restart the number, in the
!          previous calculation, of the moment to use to initialize moment
!          imom of the new calculation (by default imoold(imom)=imom).
!            Value -1 indicates the we must reinitialize moment imom.
!        ntdmom(imom) defined the time step at which the moment calculation
!          is started.

!     We give below the example of the calculation of moments <u> and <rho u v>
!       the moment <u> is reread in the restart file if we are restarting,
!         the moment <rho u v> is reinitialized to zero.
!       Moment <u> is calculated starting from time step 1000
!         Moment <rho u v> is calculated from time step 10000.


!     The test on iutile allows deactivation of the instructions
!       (which are only given as an example).

iutile = 0
if (iutile.eq.1) then

  ! First moment: <u>
  imom  = 1
  idfmom(1,imom) =  iu
  ntdmom(imom)   =  1000
  ! Second moment: <rho u v>
  imom  = 2
  idfmom(1,imom) = -irom
  idfmom(2,imom) =  iu
  idfmom(3,imom) =  iv
  imoold(imom)   = -1
  ntdmom(imom)   =  10000

endif

!----
! Formats
!----


return
end subroutine


!===============================================================================


subroutine usipes &
!================

 ( nmodpp , iverif )


!===============================================================================
! Purpose:
! --------

! User subroutine for the input of additional user parameters for
! input/output.

!-------------------------------------------------------------------------------
! Arguments
!__________________.____._____.________________________________________________.
! name             !type!mode ! role                                           !
!__________________!____!_____!________________________________________________!
! nmodpp           ! i  ! <-- ! number of active specific physics models       !
! iverif           ! i  ! <-- ! flag for elementary tests                      !
!__________________!____!_____!________________________________________________!

!     Type: i (integer), r (real), s (string), a (array), l (logical),
!           and composite types (ex: ra real array)
!     mode: <-- input, --> output, <-> modifies data, --- work array
!===============================================================================

!===============================================================================
! Module files
!===============================================================================

use paramx
use cstnum
use dimens
use numvar
use optcal
use cstphy
use entsor
use parall
use period
use ihmpre
use ppppar
use ppthch
use ppincl

!===============================================================================

implicit none

! Arguments

integer nmodpp
integer iverif

! Local variables

integer ii, ipp, imom, iutile

!===============================================================================


!===============================================================================


!     This subroutine allows setting parameters

!       which do not already appear in the other subroutines of this file.


!     It is possible to add or remove parameters.


!     The number of physical properties and variables is known here.


!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_START
!ex
!ex !     If we are using the Code_Saturne GUI:
!ex
!ex !       we will find in the user subroutines commented examples
!ex !       on the model of the present section.
!ex
!ex !       If necessary, the user may uncomment them and adapt them to
!ex !       his needs.
!ex
!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_END

!===============================================================================

!===============================================================================
! 1. Input-output (entsor.h)
!===============================================================================

! --- write auxiliary restart file iecaux = 1 yes, 0 no

!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_START
!ex
!ex iecaux = 1
!ex
!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_END


! Frequency of log output

!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_START
!ex
!ex ntlist = 1
!ex
!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_END

! Log (listing) verbosity

!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_START
!ex
!ex iutile = 0
!ex if (iutile.eq.1) then
!ex
!ex   do ii = 1, nvar
!ex     iwarni(ii) = 1
!ex   enddo
!ex
!ex   iwarni(ipr) = 2
!ex   iwarni(iu) = 2
!ex   iwarni(iv) = 2
!ex   iwarni(iw) = 2
!ex
!ex endif
!ex
!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_END

! --- history output step

!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_START
!ex
!ex nthist = 1
!ex frhist = -1.d0
!ex
!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_END


! --- Number of monitoring points (probes) and their positions
!     (limited to ncaptm=100)

!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_START
!ex
!ex ncapt  = 4
!ex tplfmt = 1 ! time plot format (1: .dat, 2: .csv, 3: both)
!ex
!ex xyzcap(1,1) = 0.30d0
!ex xyzcap(2,1) = 0.15d0
!ex xyzcap(3,1) = 0.01d0
!ex
!ex xyzcap(1,2) = 0.30d0
!ex xyzcap(2,2) = 0.00d0
!ex xyzcap(3,2) = 0.01d0
!ex
!ex xyzcap(1,3) = 0.30d0
!ex xyzcap(2,3) =-0.08d0
!ex xyzcap(3,3) = 0.01d0
!ex
!ex xyzcap(1,4) = 0.60d0
!ex xyzcap(2,4) =-0.05d0
!ex xyzcap(3,4) = 0.01d0
!ex
!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_END


! --- current variable

!     As for other variables,
!       if we do not assign the following array values,
!       default values will be used

!     nomvar( ) = variable name
!     ichrvr( ) = chonological output (yes 1/no 0)
!     ilisvr( ) = logging in listing (yes 1/no 0)
!     ihisvr( ) = history output (number of probes and their numbers)
!     if ihisvr(.,1)  = -1, output for all probes

!     Note: Only the fist 8 characters of a name will be used in the most
!           detailed log.



!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_START
!ex
!ex ! Current dynamic variables
!ex
!ex ! pressure variable
!ex ipp = ipprtp(ipr   )
!ex nomvar(ipp)   = 'Pressure'
!ex ichrvr(ipp)   = 1
!ex ilisvr(ipp)   = 1
!ex ihisvr(ipp,1) = -1
!ex if (icorio.eq.1) then
!ex   nomvar(ipp)   = 'Rel Pressure'
!ex endif
!ex
!ex ! variable v1x
!ex ipp = ipprtp(iu    )
!ex nomvar(ipp)   = 'VelocityX'
!ex ichrvr(ipp)   = 1
!ex ilisvr(ipp)   = 1
!ex ihisvr(ipp,1) = -1
!ex if (icorio.eq.1) then
!ex   nomvar(ipp)   = 'Rel VelocityX'
!ex endif
!ex
!ex ! v1y variable
!ex ipp = ipprtp(iv    )
!ex nomvar(ipp)   = 'VelocityY'
!ex ichrvr(ipp)   = 1
!ex ilisvr(ipp)   = 1
!ex ihisvr(ipp,1) = -1
!ex if (icorio.eq.1) then
!ex   nomvar(ipp)   = 'Rel VelocityY'
!ex endif
!ex
!ex ! v1z variable
!ex ipp = ipprtp(iw    )
!ex nomvar(ipp)   = 'VelocityZ'
!ex ichrvr(ipp)   = 1
!ex ilisvr(ipp)   = 1
!ex ihisvr(ipp,1) = -1
!ex if (icorio.eq.1) then
!ex   nomvar(ipp)   = 'Rel VelocityZ'
!ex endif
!ex
!ex if (itytur.eq.2) then
!ex
!ex   ! turbulent kinetic energy
!ex   ipp = ipprtp(ik    )
!ex   nomvar(ipp)   = 'Turb Kinetic Energy'
!ex   ichrvr(ipp)   = 1
!ex   ilisvr(ipp)   = 1
!ex   ihisvr(ipp,1) = -1
!ex
!ex   ! turbulent dissipation
!ex   ipp = ipprtp(iep   )
!ex   nomvar(ipp)   = 'Turb Dissipation'
!ex   ichrvr(ipp)   = 1
!ex   ilisvr(ipp)   = 1
!ex   ihisvr(ipp,1) = -1
!ex
!ex elseif (itytur.eq.3) then
!ex
!ex   ! Reynolds stresses
!ex   ipp = ipprtp(ir11  )
!ex   nomvar(ipp)   = 'R11'
!ex   ichrvr(ipp)   = 1
!ex   ilisvr(ipp)   = 1
!ex   ihisvr(ipp,1) = -1
!ex
!ex   ! Reynolds stresses
!ex   ipp = ipprtp(ir22  )
!ex   nomvar(ipp)   = 'R22'
!ex   ichrvr(ipp)   = 1
!ex   ilisvr(ipp)   = 1
!ex   ihisvr(ipp,1) = -1
!ex
!ex   ! Reynolds stresses
!ex   ipp = ipprtp(ir33  )
!ex   nomvar(ipp)   = 'R33'
!ex   ichrvr(ipp)   = 1
!ex   ilisvr(ipp)   = 1
!ex   ihisvr(ipp,1) = -1
!ex
!ex   ! Reynolds stresses
!ex   ipp = ipprtp(ir12  )
!ex   nomvar(ipp)   = 'R12'
!ex   ichrvr(ipp)   = 1
!ex   ilisvr(ipp)   = 1
!ex   ihisvr(ipp,1) = -1
!ex
!ex   ! Reynolds stresses
!ex   ipp = ipprtp(ir13  )
!ex   nomvar(ipp)   = 'R13'
!ex   ichrvr(ipp)   = 1
!ex   ilisvr(ipp)   = 1
!ex   ihisvr(ipp,1) = -1
!ex
!ex   ! Reynolds stresses
!ex   ipp = ipprtp(ir23  )
!ex   nomvar(ipp)   = 'R23'
!ex   ichrvr(ipp)   = 1
!ex   ilisvr(ipp)   = 1
!ex   ihisvr(ipp,1) = -1
!ex
!ex   ! turbulent dissipation
!ex   ipp = ipprtp(iep   )
!ex   nomvar(ipp)   = 'Turb Dissipation'
!ex   ichrvr(ipp)   = 1
!ex   ilisvr(ipp)   = 1
!ex   ihisvr(ipp,1) = -1
!ex
!ex elseif (iturb.eq.50) then
!ex
!ex   ! turbulent kinetic energy
!ex   ipp = ipprtp(ik    )
!ex   nomvar(ipp)   = 'Turb Kinetic Energy'
!ex   ichrvr(ipp)   = 1
!ex   ilisvr(ipp)   = 1
!ex   ihisvr(ipp,1) = -1
!ex
!ex   ! turbulent dissipation
!ex   ipp = ipprtp(iep   )
!ex   nomvar(ipp)   = 'Turb Dissipation'
!ex   ichrvr(ipp)   = 1
!ex   ilisvr(ipp)   = 1
!ex   ihisvr(ipp,1) = -1
!ex
!ex   ! phi
!ex   ipp = ipprtp(iphi  )
!ex   nomvar(ipp)   = 'Phi'
!ex   ichrvr(ipp)   = 1
!ex   ilisvr(ipp)   = 1
!ex   ihisvr(ipp,1) = -1
!ex
!ex   ! f_bar
!ex   ipp = ipprtp(ifb   )
!ex   nomvar(ipp)   = 'f_bar'
!ex   ichrvr(ipp)   = 1
!ex   ilisvr(ipp)   = 1
!ex   ihisvr(ipp,1) = -1
!ex
!ex elseif (iturb.eq.51) then
!ex
!ex   ! turbulent kinetic energy
!ex   ipp = ipprtp(ik    )
!ex   nomvar(ipp)   = 'Turb Kinetic Energy'
!ex   ichrvr(ipp)   = 1
!ex   ilisvr(ipp)   = 1
!ex   ihisvr(ipp,1) = -1
!ex
!ex   ! turbulent dissipation
!ex   ipp = ipprtp(iep   )
!ex   nomvar(ipp)   = 'Turb Dissipation'
!ex   ichrvr(ipp)   = 1
!ex   ilisvr(ipp)   = 1
!ex   ihisvr(ipp,1) = -1
!ex
!ex   ! phi
!ex   ipp = ipprtp(iphi  )
!ex   nomvar(ipp)   = 'Phi'
!ex   ichrvr(ipp)   = 1
!ex   ilisvr(ipp)   = 1
!ex   ihisvr(ipp,1) = -1
!ex
!ex   ! alpha
!ex   ipp = ipprtp(ial   )
!ex   nomvar(ipp)   = 'Alpha'
!ex   ichrvr(ipp)   = 1
!ex   ilisvr(ipp)   = 1
!ex   ihisvr(ipp,1) = -1
!ex
!ex elseif (iturb.eq.60) then
!ex
!ex   ! turbulent kinetic energy
!ex   ipp = ipprtp(ik    )
!ex   nomvar(ipp)   = 'Turb Kinetic Energy'
!ex   ichrvr(ipp)   = 1
!ex   ilisvr(ipp)   = 1
!ex   ihisvr(ipp,1) = -1
!ex
!ex   ! omega
!ex   ipp = ipprtp(iomg  )
!ex   nomvar(ipp)   = 'Omega'
!ex   ichrvr(ipp)   = 1
!ex   ilisvr(ipp)   = 1
!ex   ihisvr(ipp,1) = -1
!ex
!ex elseif (iturb.eq.70) then
!ex
!ex   ! Spalart-Allmaras variable (viscosity-like)
!ex   ipp = ipprtp(inusa )
!ex   nomvar(ipp)   = 'NuTilda'
!ex   ichrvr(ipp)   = 1
!ex   ilisvr(ipp)   = 1
!ex   ihisvr(ipp,1) = -1
!ex
!ex endif
!ex
!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_END

! User scalar variables.

! We may modify here the arrays relative to user scalars, but scalars
!   reserved for specific physics are handled automatically. This explains
!   the tests on 'nscaus', which ensure that the targeted scalars are
!   truly user scalars.
! By specific physics, we mean only those which are handled in specific
!   modules of the code, such as coal, combustion, electric arcs (see usppmo).

!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_START
!ex
!ex if (isca(1).gt.0.and.nscaus.ge.1) then
!ex   ipp = ipprtp(isca  (1))
!ex   nomvar(ipp)  = 'Scalar 1'
!ex   ichrvr(ipp)  = 1
!ex   ilisvr(ipp)  = 1
!ex   ihisvr(ipp,1)= -1
!ex endif
!ex
!ex if (isca(2).gt.0.and.nscaus.ge.2) then
!ex   ipp = ipprtp(isca  (2))
!ex   nomvar(ipp)  = 'Scalar 2'
!ex   ichrvr(ipp)  = 1
!ex   ilisvr(ipp)  = 1
!ex   ihisvr(ipp,1)= -1
!ex endif
!ex
!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_END


! Other variables

!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_START
!ex
!ex ! Density variable (output for post-processing only if variable or
!ex !                   in the case of specific physics)
!ex ipp = ipppro(ipproc(irom  ))
!ex nomvar(ipp)   = 'Density'
!ex ichrvr(ipp)   = max(irovar,nmodpp)
!ex ilisvr(ipp)   = 1
!ex ihisvr(ipp,1) = -1
!ex
!ex ! specific heat
!ex if (icp   .gt.0) then
!ex   ipp = ipppro(ipproc(icp   ))
!ex   nomvar(ipp)   = 'Specific Heat'
!ex   ichrvr(ipp)   = 0
!ex   ilisvr(ipp)   = 0
!ex   ihisvr(ipp,1) = 0
!ex endif
!ex
!ex ! laminar viscosity
!ex ipp = ipppro(ipproc(iviscl))
!ex nomvar(ipp)   = 'Laminar Viscosity'
!ex ichrvr(ipp)   = 0
!ex ilisvr(ipp)   = 0
!ex ihisvr(ipp,1) = 0
!ex
!ex ! turbulent viscosity
!ex ipp = ipppro(ipproc(ivisct))
!ex nomvar(ipp)   = 'Turb Viscosity'
!ex ichrvr(ipp)   = 1
!ex ilisvr(ipp)   = 1
!ex ihisvr(ipp,1) = -1
!ex
!ex ! Courant number
!ex ipp = ipppro(ipproc(icour))
!ex nomvar(ipp)   = 'CFL'
!ex ichrvr(ipp)   = 1
!ex ilisvr(ipp)   = 0
!ex ihisvr(ipp,1) = -1
!ex
!ex ! Fourier number
!ex ipp = ipppro(ipproc(ifour))
!ex nomvar(ipp)   = 'Fourier Number'
!ex ichrvr(ipp)   = 1
!ex ilisvr(ipp)   = 0
!ex ihisvr(ipp,1) = -1
!ex
!ex ! 'csmago' variable for dynamic L.E.S. models
!ex !    (square of the Samgorinsky "constant")
!ex if (ismago.gt.0) then
!ex   ipp = ipppro(ipproc(ismago))
!ex   nomvar(ipp)   = 'Csdyn2'
!ex   ichrvr(ipp)   = 1
!ex   ilisvr(ipp)   = 1
!ex   ihisvr(ipp,1) = -1
!ex endif
!ex
!ex ! temporal means (example for moment 1)
!ex if (nbmomt.gt.0) then
!ex   imom = 1
!ex   ipp = ipppro(ipproc(icmome(imom)))
!ex   nomvar(ipp) = 'Time Average 01'
!ex   ichrvr(ipp) = 1
!ex   ilisvr(ipp) = 1
!ex   ihisvr(ipp,1) = -1
!ex endif
!ex
!ex ! total pressure (not defined in compressible case)
!ex if (ippmod(icompf).lt.0) then
!ex   ipp = ipppro(ipproc(iprtot))
!ex   nomvar(ipp)   = 'Total Pressure'
!ex   ichrvr(ipp)   = 1
!ex   ilisvr(ipp)   = 1
!ex   ihisvr(ipp,1) = -1
!ex endif
!ex
!ex ! local time step
!ex ipp = ippdt
!ex nomvar(ipp)   = 'Local Time Step'
!ex ichrvr(ipp)   = 1
!ex ilisvr(ipp)   = 1
!ex ihisvr(ipp,1) = -1
!ex
!ex ! characteristic time of transient velocity/pressure coupling
!ex ipp = ipptx
!ex nomvar(ipp)   = 'Tx'
!ex ichrvr(ipp)   = 1
!ex ilisvr(ipp)   = 1
!ex ihisvr(ipp,1) = -1
!ex
!ex ipp = ippty
!ex nomvar(ipp)   = 'Ty'
!ex ichrvr(ipp)   = 1
!ex ilisvr(ipp)   = 1
!ex ihisvr(ipp,1) = -1
!ex
!ex ipp = ipptz
!ex nomvar(ipp)   = 'Tz'
!ex ichrvr(ipp)   = 1
!ex ilisvr(ipp)   = 1
!ex ihisvr(ipp,1) = -1
!ex
!ex ! EXAMPLE_CODE_TO_BE_ADAPTED_BY_THE_USER_END


!----
! Formats
!----



return
end subroutine
