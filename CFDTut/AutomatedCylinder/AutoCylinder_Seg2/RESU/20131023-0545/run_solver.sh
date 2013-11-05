#!/bin/bash


# Detect and handle running under SALOME YACS module.
YACS_ARG=
if test "$SALOME_CONTAINERNAME" != "" -a "$CFDRUN_ROOT_DIR" != "" ; then
  YACS_ARG="--yacs-module=${CFDRUN_ROOT_DIR}"/lib/salome/libCFD_RunExelib.so
fi

# Export paths here if necessary or recommended.

cd /home/vance/Downloads/Capstone/MCCapstone13-14/CFDTut/AutomatedCylinder/AutoCylinder_Seg2/RESU/20131023-0545

# Run solver.
mpiexec.openmpi -n 2 /usr/lib/code_saturne/cs_solver --param alt_script_2.xml --mpi $YACS_ARGS $@

CS_RET=$?

exit $CS_RET

