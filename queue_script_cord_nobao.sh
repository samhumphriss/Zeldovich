#!/bin/bash -l
#BSUB -L /bin/bash
#BSUB -q cordelia
#BSUB -n 1 #Number of processors
#BSUB -J zeldovich_stats_nobao[1-300] #Job name
#BSUB -eo ./dump/zeldovich_stats_nobao%I.err #Error outputs
#BSUB -oo ./dump/zeldovich_stats_nobao%I.out #Program outputs
#BSUB -P durham
#BSUB -R "span[hosts=1]" #Processors per node
#BSUB -W 02:00 #Wall clock time

folderloc="/gpfs/data/rhgk18/results/Troubleshoot"

mkdir $folderloc
mkdir "$folderloc/nobao"

. /etc/profile.d/modules.sh
module purge
module load python/2.7.3

python exeMAIN.py -b 512 -g 256 -r -f "$folderloc/nobao" -p "nowig.txt" --runindex ${LSB_JOBINDEX}
