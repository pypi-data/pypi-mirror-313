#!/bin/bash

# Path to your conda installation
CONDA_PATH="$HOME/miniconda3"

# Activate the conda environment
source "$CONDA_PATH/bin/activate" mdc

# Set the environment variable
export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libstdc++.so.6

# Run the executable
aloha_data_collection
