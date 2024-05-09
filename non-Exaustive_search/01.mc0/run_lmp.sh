#!/bin/bash
home_dir=$(pwd)
signature=$0
#script_dir=
#tmp_dir=
#mkdir 

#read -p "enter the prefix: " prefix
#read -p "enter the ref pwin file: " f_ref

#--------------------------------------------------------

cifs_to_datas.py << EOF
blank.xyz
EOF

ln -s ../../OC_10M.pb ./
cp ../../uniq_element_list ./


type_map=$(cat uniq_element_list)

all_adjust_data_file_by_ele_list.sh << EOF
$type_map
EOF

cp ../../ref_lmp/in.lammps.template in.lammps

#
dirname=$(basename `pwd`)
grep_patten=$(echo $dirname | sed "s/_/|/g")
echo "grep_patten = $grep_patten"
mc_atoms_index=$(grep -E "$grep_patten" in.lammps | awk -F ' ' '{print $2}' | xargs)
sed -i "s/mc_atoms_index_put_here/${mc_atoms_index}/g" in.lammps


mkdir traj

job_num_control
sub_dp_lmp_v2.22
