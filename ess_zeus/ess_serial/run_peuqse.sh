#!/bin/bash
#SBATCH --job-name=PEUQSE_ESS_PARALLEL
#SBATCH --error=error.log
#SBATCH --partition=short,west,sharing
#SBATCH --mem=20Gb
#SBATCH --time=00:30:00
#SBATCH --cpus-per-task=1
#SBATCH --ntasks=8
#SBATCH --tasks-per-node=8


#python run_peuqse.py
mpiexec -n 8 -v python run_peuqse.py

