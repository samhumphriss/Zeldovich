#!/bin/bash -l
#BSUB -L /bin/bash
#BSUB -q cordelia
#BSUB -n 1 #Number of processors
#BSUB -J zeldovich_stats_bao[1-300] #Job name
#BSUB -eo ./dump/b1024_ng256_np256/zeldovich_b%I.err #Error outputs
#BSUB -oo ./dump/b1024_ng256_np256/zeldovich_b%I.out #Program outputs
#BSUB -P durham
#BSUB -R "span[ptile=2]" #Processors per node
#BSUB -W 02:00 #Wall clock

ulimit -c 0

folderloc="/gpfs/data/rhgk18/results/b1024_ng256_np256_t300"

mkdir $folderloc
mkdir "$folderloc/bao"

. /etc/profile.d/modules.sh
module purge
module load python/2.7.3

python exeMAIN.py -b 1024 -g 256 -np 256 -r -f "$folderloc/bao" -p "wig.txt" --runindex ${LSB_JOBINDEX}
