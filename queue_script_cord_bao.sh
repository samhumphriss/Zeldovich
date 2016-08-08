#!/bin/bash -l
#BSUB -L /bin/bash
#BSUB -q cordelia
#BSUB -n 1 #Number of processors
#BSUB -J zeldovich_stats_bao[1-300] #Job name
#BSUB -eo ./dump/zeldovich_stats_bao%I.err #Error outputs
#BSUB -oo ./dump/zeldovich_stats_bao%I.out #Program outputs
#BSUB -P durham
#BSUB -R "span[hosts=1]" #Processors per node
#BSUB -W 02:00 #Wall clock time

. /etc/profile.d/modules.sh
module purge
module load python/2.7.3

python exeMAIN.py -b 512 -g 256 -r -f "/B512_G256_003/bao" -p "wig.txt" --runindex ${LSB_JOBINDEX}
