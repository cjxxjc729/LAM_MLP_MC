#!/bin/bash
home_dir=$(pwd)
signature=$0
#script_dir=
#tmp_dir=
#mkdir 

#read -p "enter the prefix: " prefix
#read -p "enter the ref pwin file: " f_ref

#--------------------------------------------------------

lpj_file_name=1_1000.lammpstrj

cd ../01.mc/
 
  if [ -d ${lpj_file_name}_coll ]
  then
    rm -r ${lpj_file_name}_coll
  fi

  digfs << EOF
${lpj_file_name}
-2
EOF

  cd ${lpj_file_name}_coll 

  fs_lpj=$(lxargs lammpstrj)

  cp ../uniq_element_list ./
  lpj-trj_to_xyz.for_dpa.py $fs_lpj

cd $home_dir

mkdir xyz_files
cp ../01.mc/${lpj_file_name}_coll/*xyz xyz_files

cd xyz_files
  
  grep elements_pool ../../01.mc/input.parameters | awk -F '=' '{print $2}' | sed "s/ /\n/g" > ele_list
 
  ../step1.Af_matrix_calculation.py
  ../step2.py
  ../step3.py
  ../step4.swap.py
  
  
