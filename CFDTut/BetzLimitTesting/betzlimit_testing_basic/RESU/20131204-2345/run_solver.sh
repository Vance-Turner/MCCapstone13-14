#!/bin/bash


# Detect and handle running under SALOME YACS module.
YACS_ARG=
if test "$SALOME_CONTAINERNAME" != "" -a "$CFDRUN_ROOT_DIR" != "" ; then
  YACS_ARG="--yacs-module=${CFDRUN_ROOT_DIR}"/lib/salome/libCFD_RunExelib.so
fi

# Export paths here if necessary or recommended.

cd /home/vance/Downloads/Capstone/MCCapstone13-14/CFDTut/BetzLimitTesting/betzlimit_testing_basic/RESU/20131204-2345

# Run solver.
mpiexec.openmpi -n 2 /usr/lib/code_saturne/cs_solver --param betzlimit_cylinder_basic.xml --mpi $YACS_ARGS $@

CS_RET=$?

exit $CS_RET

