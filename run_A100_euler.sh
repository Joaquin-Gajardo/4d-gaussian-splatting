#!/bin/bash
#SBATCH -J realtime4dgs
#SBATCH --mail-type=END,FAIL
#SBATCH --time=48:00:00
#SBATCH --gpus=1 
#SBATCH --gres=gpumem:80g
#SBATCH --mem-per-cpu=8G
#SBATCH --cpus-per-task=4
#SBATCH --output=sbatch_log/%j.out
#SBATCH --error=sbatch_log/%j.out

module purge

/cluster/project/cropsci/jgajardo/miniconda3/bin/conda init
conda activate base
conda activate realtime4dgs2 # this doesn't work, need to activate environment in terminal where I send the job with sbatch run.sh and then it works
conda list

module load stack/2024-04
module load gcc/8.5.0 cuda/11.8.0 ninja/1.11.1 eth_proxy
echo $(module list)

nvidia-smi

#bash train_WAT.sh 

experiment_name="$1"
mod_args="$2"

bash run_WAT_experiment_euler.sh "$experiment_name" "$mod_args"