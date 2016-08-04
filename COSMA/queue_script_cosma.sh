#!/bin/bash -l
#BSUB -L /bin/bash
#BSUB -q cordelia
#BSUB -n 1 #Number of processors
#BSUB -J zeldovich_stats[1-10] #Job name
#BSUB -eo zeldovich_stats_%I.err #Error outputs
#BSUB -oo zeldovich_stats_%I.out #Program outputs
#BSUB -P durham
#BSUB -R "ptile[hosts=1]" #Processors per node
#BSUB -W 01:00 #Wall clock time

. /etc/profile.d/modules.sh
module purge
module load python/2.7.3

python runcode.py runindex=${LSB_JOBINDEX} -g 128 -b 512 -r -f "/B512_G128_001"
