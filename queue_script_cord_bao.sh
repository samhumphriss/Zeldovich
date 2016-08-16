#!/bin/bash -l
#BSUB -L /bin/bash
#BSUB -q cordelia
#BSUB -n 1 #Number of processors
#BSUB -J zeldovich_stats_bao[1] #Job name
#BSUB -eo ./dump/upd_zeldovich_b%I.err #Error outputs
#BSUB -oo ./dump/upd_zeldovich_b%I.out #Program outputs
#BSUB -P durham
#BSUB -R "span[hosts=1]" #Processors per node
#BSUB -W 01:00 #Wall clock time

ulimit -c 0

folderloc="/gpfs/data/rhgk18/results/upd_trial100_2"

mkdir $folderloc
mkdir "$folderloc/bao"

. /etc/profile.d/modules.sh
module purge
module load python/2.7.3

python exeMAIN.py -b 1024 -g 256 -np 512 -r -f "$folderloc/bao" -p "wig.txt" --runindex ${LSB_JOBINDEX}
