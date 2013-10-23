#!/bin/bash


# Detect and handle running under SALOME YACS module.
YACS_ARG=
if test "$SALOME_CONTAINERNAME" != "" -a "$CFDRUN_ROOT_DIR" != "" ; then
  YACS_ARG="--yacs-module=${CFDRUN_ROOT_DIR}"/lib/salome/libCFD_RunExelib.so
fi

# Export paths here if necessary or recommended.

cd /home/vance/Capstone13-14/MCCapstone13-14/CFDTut/AutomatedCylinder/AutoCylinder/RESU/20131021-1656

# Run solver.
mpiexec.openmpi -n 4 /home/vance/Capstone13-14/MCCapstone13-14/CFDTut/AutomatedCylinder/AutoCylinder/RESU/20131021-1656/cs_solver --param script_tria_mesh --mpi $YACS_ARGS $@

CS_RET=$?

exit $CS_RET

