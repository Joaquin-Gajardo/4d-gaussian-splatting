#!/bin/bash
#SBATCH -J setup
#SBATCH --time=1:00:00
#SBATCH --gpus=1
#SBATCH --mem-per-cpu=4G
#SBATCH --cpus-per-task=4
#SBATCH --output=./output/setup.out
 
module load gcc/8.2.0 cuda/11.6.2 glm/0.9.7.1 ninja/1.10.2 eth_proxy
echo $(module list)

source ~/.bashrc
conda activate base

conda activate realtime4DGS

#pip install --no-cache-dir ./diff-gaussian-rasterization
pip install --no-cache-dir ./simple-knn

# Optional: packages for realtime 4DGS (https://github.com/fudan-zvg/4d-gaussian-splatting)
pip install tqdm==4.66.1
pip install torchmetrics==0.11.4
pip install imagesize==1.4.1
pip install kornia==0.6.12
pip install omegaconf==2.3.0
pip install --no-cache-dir ./pointops2