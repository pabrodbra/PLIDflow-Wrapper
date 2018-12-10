#!/bin/bash

if [[ $# -ne 2 ]] ; then
    echo '*** ERROR *** USAGE :: prepare_workflow.sh <Protein-Ligand_CSV> <Output_Path>'
    exit -1
fi

PROTEING_LIGAND_LIST=$1
OUTPUT_PATH=$2
DOWNLOAD_SCRIPT="python get_pd_files.py"
PYMOL_SCRIPT="pymol -c remove-ligand.pml"

mkdir -p $OUTPUT_PATH

while IFS=',' read -r PDB LIG
do
    ${DOWNLOAD_SCRIPT} ${PDB} ${LIG} "${OUTPUT_PATH}/"
    ${PYMOL_SCRIPT} -- "${OUTPUT_PATH}/${PDB}.pdb" ${LIG} "${OUTPUT_PATH}/${PDB%.pdb}_Protein.pdb" > /dev/null
done < $PROTEING_LIGAND_LIST