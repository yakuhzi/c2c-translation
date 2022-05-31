#!/bin/bash
#SBATCH --ntasks=10
#SBATCH --time=3:00:00
#SBATCH --mem=80GB
#SBATCH --gres=gpu:1
#SBATCH --job-name=c_st_python_java
#SBATCH --output=c_st_python_java_%j.out

python -m codegen_sources.scripts.corrections.corrections -s python -t java