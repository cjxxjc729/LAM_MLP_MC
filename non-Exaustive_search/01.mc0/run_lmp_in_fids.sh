#!/bin/bash
home_dir=$(pwd)
signature=$0
script_dir=$(realpath ./)
#tmp_dir=
#mkdir 

#read -p "enter the prefix: " prefix
#read -p "enter the ref pwin file: " f_ref

#--------------------------------------------------------
cd material_lmp 
  home_dir1=$(pwd)

  fids=$(lld | xargs)

  for fid in $fids
  do
    cd $fid
      if [ ! -f lmp.out ]
      then
        ${script_dir}/run_lmp.sh
      fi
    cd $home_dir1
  done

  holdon_wait_following_dir_done_V2.sh


