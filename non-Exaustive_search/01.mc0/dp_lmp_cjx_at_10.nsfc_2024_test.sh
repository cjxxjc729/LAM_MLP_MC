#!/bin/bash
#SBATCH -p v6_384
#SBATCH -N 1
#SBATCH -n 16
export PATH=/public1/home/sch0149/deepmd-kit-2.2.9/bin:$PATH
export OMP_NUM_THREADS=16
source /public1/home/sch0149/deepmd-kit-2.2.9/bin/activate /public1/home/sch0149/deepmd-kit-2.2.9/
#source activate deepmd-kit

lmp -i in.lammps > lmp.out



