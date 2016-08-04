#!/bin/bash -l
#BSUB -L /bin/bash
#BSUB -q cordelia
#BSUB -n 1 #Number of processors
#BSUB -J zeldovich_stats[1-10] #Job name
#BSUB -eo ./dump/zeldovich_stats_%I.err #Error outputs
#BSUB -oo ./dump/zeldovich_stats_%I.out #Program outputs
#BSUB -P durham
#BSUB "ptile[hosts=1]" #Processors per node
#BSUB -W 00:10 #Wall clock time

. /etc/profile.d/modules.sh
module purge
module load python/2.7.3

python exeCORDELIA.py -b 512 -g 128 -r -f "/B512_G128_001"
