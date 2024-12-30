# RAG-APP1

This is a minimal implementation of the RAG model for question answering

## Requirments

- Python 3.8 or higher

#### Install Python using Miniconda (Linux)

1) These four commands download the latest 64-bit version of the Miniconda Linux installer, rename it to a shorter file name, silently install, and then delete the installer:

```bash
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda3/miniconda.sh
```

2) Create and activate new environment using the following commands:

```bash

# Activate a Conda environment
source ~/miniconda3/bin/activate

# Create a new environment with Python 3.8
conda create -n rag-app1 python=3.8

# Activate the environment
conda activate rag-app1
```
