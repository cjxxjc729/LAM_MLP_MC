#!/bin/bash
home_dir=$(pwd)
signature=$0
#script_dir=
#tmp_dir=
#mkdir 

#read -p "enter the prefix: " prefix
#read -p "enter the ref pwin file: " f_ref

#--------------------------------------------------------

if [ ! -d cif_coll ]
then
    # step 1
    echo "step 1 get_combinations.py"
    ./script/get_combinations.py >> /dev/null

    # step 2
    echo "step 2: create_data_files.sh"
    ./script/01.create_data_files.sh >> /dev/null
else
    echo "skip step 1 and step 2"
fi

# step 3
if [ ! -f lmp_main/mc.done ]
then
    echo "step 3: run mc"
    ./script/02.run_mc >> /dev/null
else
    echo "skip step 3"
fi

# step 4
echo "step 4: mc_pp"
./script/02.mc_pp.sh >> /dev/null

#5
if [ ! -d single_metal_energies ]
then
    echo "step 5: get_single_atoms_energy"
    ./script/04.get_single_atoms_energy.main.sh    
else
    echo "skip step 5"
fi



