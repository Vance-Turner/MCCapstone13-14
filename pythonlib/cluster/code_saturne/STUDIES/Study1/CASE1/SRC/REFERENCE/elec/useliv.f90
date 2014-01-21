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

subroutine useliv &
!================

 ( nvar   , nscal  ,                                              &
   dt     , rtp    , propce , propfa , propfb , coefa  , coefb  )

!===============================================================================
! Purpose :
! --------

! variables initialization for specific electric module :
!    the same as USINIV.F for main variables

! Cette routine est appelee en debut de calcul (suite ou non)
!     avant le debut de la boucle en temps

! Elle permet d'INITIALISER ou de MODIFIER (pour les calculs suite)
!     les variables de calcul (inconnues transportees),
!     la valeur du pas de temps,

! On a repris a titre d'exemple dans cette routine utilisateur
!     l'initialisation choisie par defaut.
!

! Thermodynamic properties and transport coefficients are in
!     PROPCE (at the center of the cells), PROPFA (for internal faces),
!     PROPFB (prop aux faces de bord)
!     Ainsi,
!      PROPCE(IEL,IPPROC(IROM  )) designe ROM   (IEL)
!      PROPCE(IEL,IPPROC(IVISCL)) designe VISCL (IEL)
!      PROPCE(IEL,IPPROC(ICP   )) designe CP    (IEL)
!      PROPCE(IEL,IPPROC(IVISLS(ISCAL))) designe VISLS (IEL ,ISCAL)

!      PROPFA(IFAC,IPPROF(IFLUMA(IVAR ))) designe FLUMAS(IFAC,IVAR)

!      PROPFB(IFAC,IPPROB(IROM  )) designe ROMB  (IFAC)
!      PROPFB(IFAC,IPPROB(IFLUMA(IVAR ))) designe FLUMAB(IFAC,IVAR)

! Thermodynamic properties and transport coefficients modification
!  (ROM, VISCL, VISCLS, CP) will be done by default in  PPPHYV
!     and not here


! Cells identification
! ====================

! Cells may be identified using the 'getcel' subroutine.
! The syntax of this subroutine is described in the 'usclim' subroutine,
! but a more thorough description can be found in the user guide.


!-------------------------------------------------------------------------------
! Arguments
!__________________.____._____.________________________________________________.
!    nom           !type!mode !                   role                         !
!__________________!____!_____!________________________________________________!
! nvar             ! e  ! <-- ! nombre total de variables                      !
! nscal            ! e  ! <-- ! nombre total de scalaires                      !
! dt(ncelet)       ! tr ! <-- ! valeur du pas de temps                         !
! rtp              ! tr ! <-- ! variables de calcul au centre des              !
! (ncelet,*)       !    !     !    cellules                                    !
! propce           ! tr ! <-- ! proprietes physiques au centre des             !
! (ncelet,*)       !    !     !    cellules                                    !
! propfa           ! tr ! <-- ! proprietes physiques au centre des             !
!  (nfac,*)        !    !     !    faces internes                              !
! propfb           ! tr ! <-- ! proprietes physiques au centre des             !
!  (nfabor,*)      !    !     !    faces de bord                               !
! coefa coefb      ! tr ! <-- ! conditions aux limites aux                     !
!  (nfabor,*)      !    !     !    faces de bord                               !
!__________________!____!_____!________________________________________________!

!     TYPE : E (ENTIER), R (REEL), A (ALPHANUMERIQUE), T (TABLEAU)
!            L (LOGIQUE)   .. ET TYPES COMPOSES (EX : TR TABLEAU REEL)
!     MODE : <-- donnee, --> resultat, <-> Donnee modifiee
!            --- tableau de travail
!===============================================================================

!===============================================================================
! Module files
!===============================================================================

use paramx
use pointe
use numvar
use optcal
use cstphy
use cstnum
use entsor
use parall
use period
use ppppar
use ppthch
use ppincl
use elincl
use mesh

!===============================================================================

implicit none

integer          nvar   , nscal

double precision dt(ncelet), rtp(ncelet,*), propce(ncelet,*)
double precision propfa(nfac,*), propfb(nfabor,*)
double precision coefa(nfabor,*), coefb(nfabor,*)

! Local variables

integer          iel, mode
integer          iesp , idimve

double precision tinit, hinit, coefe(ngazem)

integer, allocatable, dimension(:) :: lstelt

!===============================================================================



!===============================================================================
! 0. Control output
!===============================================================================

write(nfecra,9001)

!===============================================================================
! 1.  Local variables initialization
!===============================================================================

! Allocate a temporary array for cells selection
allocate(lstelt(ncel))


!===============================================================================
! 2. Initialization : examples
!      only at the beginning of the calculation
!===============================================================================

if ( isuite.eq.0 ) then

! --> Enthalpy = H(T0) ou 0

!     For electric arc,
!     for the whole compution domain enthalpy is set to H(T0) of the 1st constituant of the gas
!
!     For Joule jeating by direct conduction,
!     enthalpy is set to zero, and the user will enter his H(T) function tabulation.
!
!   --  HINIT calculations

  if ( ippmod(ielarc).ge.1 ) then
    mode = -1
    tinit = t0
    coefe(1) = 1.d0
    if ( ngazg .gt. 1 ) then
      do iesp = 2, ngazg
        coefe(iesp) = 0.d0
      enddo
    endif
    call elthht(mode,ngazg,coefe,hinit,tinit)
  else
    mode = -1
    tinit = t0
    call usthht(mode,hinit,tinit)
  endif

!    -- Entahlpy value

  do iel = 1, ncel
    rtp(iel,isca(ihm)) = hinit
  enddo


! --> Mass fraction  = 1 ou 0

  if ( ngazg .gt. 1 ) then
    do iel = 1, ncel
      rtp(iel,isca(iycoel(1))) = 1.d0
    enddo
    do iesp = 2, ngazg-1
      do iel = 1, ncel
        rtp(iel,isca(iycoel(iesp))) = 0.d0
      enddo
    enddo
  endif


! --> Electric potentials = 0

!     -- Real Component
  do iel = 1, ncel
    rtp(iel,isca(ipotr)) = 0.d0
  enddo

!     -- Imaginary (for Joule heating by direct conduction)
  if ( ippmod(ieljou).eq.2 .or. ippmod(ieljou).eq.4 ) then
    do iel = 1, ncel
      rtp(iel,isca(ipoti)) = 0.d0
    enddo
  endif

!     -- Vector potential (3D electric arc 3D)
  if ( ippmod(ielarc).ge.2 ) then
    do idimve = 1, ndimve
      do iel = 1, ncel
        rtp(iel,isca(ipotva(idimve))) = 0.d0
      enddo
    enddo
  endif

endif

!----
! FORMATS
!----

 9001 format(/,                                                   &
'                       ELECTRIC MODULE                       ',/,&
'  useliv : variables initialization by user                   ',/,&
'                                                             '  )

!----
! FIN
!----

! Deallocate the temporary array
deallocate(lstelt)

return
end subroutine
