# RAG-APP1

This is a minimal implementation of the RAG model for question answering

## Requirments

- Python 3.13 or higher

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

# Create a new environment with Python 3.13.1
conda create -n rag-app1 python=3.13.1

# Activate the environment
conda activate rag-app1
```

#### Install required packages
To install the required packages, run the following command:

```bash
pip install -r requirements.txt
```

Make sure you have a `requirements.txt` file in your project directory with the necessary dependencies listed.

#### Setup environment variables
To set up environment variables, you can create a `.env` file in the root directory of your project. Use the `.env.example` file as a template. Copy the `.env.example` file to `.env` and update the values as needed.

```bash
cp .env.example .env
```

Edit the `.env` file to configure your environment variables. For example:

```
API_KEY="your_api_key_here"
```

Make sure to keep the `.env` file secure and do not commit it to version control.

## Run FastAPI Surver

To run the app, use the following command:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

## POSTMAN Collection

Download the POSTMAN collection from [/assets/mini-rag-app.postman_collection.json](/assets/mini-rag-app.postman_collection.json)


## Optional steps

#### Setup your command line for better readability

To customize your command line prompt for better readability, you can set the `PS1` variable in your shell configuration file (e.g., `.bashrc` or `.bash_profile`). 

to display: The username in green, The hostname in blue., The current directory in blue, The current Git branch in purple., The current time (HH:MM:SS) in yellow., Followed by a new line and the prompt symbol.

```bash
PS1='\[\e[0;32m\]\u@\h \[\e[0;34m\]\w\[\e[0;35m\]$(__git_ps1 " (%s)") \[\e[0;33m\]\t\[\e[0m\]\n\[\033[00m\]\$ '
```
