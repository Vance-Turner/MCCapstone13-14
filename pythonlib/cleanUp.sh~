#!/bin/sh
echo "Cleaning up after generation:"$1
mkdir /home/vance/warehouse/Capstone/Mar13_Gen1
mkdir /home/vance/warehouse/Capstone/Mar13_Gen1/cluster
mkdir /home/vance/warehouse/Capstone/Mar13_Gen1/cluster/STUDIES
mkdir Gen$1_data
mv slurm* Gen$1_data
mv postprocessing* Gen$1_data
mv *_CASE Gen$1_data
mv Gen$1_data /home/vance/warehouse/Capstone/Mar12_Gen2
cd cluster/code_saturne/STUDIES
mkdir /home/vance/warehouse/Capstone/Mar13_Gen1/cluster/STUDIES/Gen$1_studies
mv * /home/vance/warehouse/Capstone/Mar13_Gen1/cluster/STUDIES/Gen$1_studies
