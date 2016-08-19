#!/bin/bash -l
#BSUB -L /bin/bash
#BSUB -q cordelia
#BSUB -n 3 #Number of processors
#BSUB -J zeldovich_512_512_1024_b[1-300] #Job name
#BSUB -eo ./dump/b512_ng512_np1024/zeldovich_b%I.err #Error outputs
#BSUB -oo ./dump/b512_ng512_np1024/zeldovich_b%I.out #Program outputs
#BSUB -P durham
#BSUB -R "span[hosts=1]" #Processors per node
#BSUB -W 00:30 #Wall clock

bs=512
ng=512
np=1024

folderloc="/gpfs/data/rhgk18/results/b${bs}_ng${ng}_np${np}"

mkdir "./dump/b${bs}_ng${ng}_np${np}"
mkdir $folderloc
mkdir "$folderloc/bao"

ulimit -c 0

. /etc/profile.d/modules.sh
module purge
module load python/2.7.3

python exeMAIN.py -b $bs -g $ng -np $np -r -f "$folderloc/bao" -p "wig.txt" --runindex ${LSB_JOBINDEX}
