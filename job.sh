#!/bin/bash
#SBATCH --out="data/slurm-%j.out"
#SBATCH --partition=week
#SBATCH --time=5-00:00:00
#SBATCH --job-name=Q_ROOTS
#SBATCH --cpus-per-task 1
#SBATCH --mem-per-cpu=10G
#SBATCH --gres=gpu:0

module purge
module load miniconda

conda activate rutabaga
python root_finder.py
