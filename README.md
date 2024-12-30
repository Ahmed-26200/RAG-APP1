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

## Optional prompet steps

## Setup your command line for better readability

To customize your command line prompt for better readability, you can set the `PS1` variable in your shell configuration file (e.g., `.bashrc` or `.bash_profile`). 

1) To change your prompt to display the username in green, the hostname in blue, and the current working directory in blue.

```bash
PS1='\[\e[0;32m\]\u@\h \[\e[0;34m\]\w\[\e[0m\] \$ '
```

2) To customize the Bash prompt to show the username, hostname, and current directory in bright green, followed by a new line and the prompt symbol:

```bash
PS1='\[\033[01;32m\]\u@\h:\w\n\[\033[00m\]\$ '
```

3) Simple Prompt with Time: display the username in green, hostname in blue, current directory in blue, and the current time in yellow.

```bash
PS1='\[\e[0;32m\]\u@\h \[\e[0;34m\]\w \[\e[0;33m\]\t\[\e[0m\] \$ '
```

4) Prompt with Git Branch: This will display the username in green, hostname in blue, current directory in blue, and the current Git branch in purple (requires git-prompt.sh).

```bash
PS1='\[\e[0;32m\]\u@\h \[\e[0;34m\]\w\[\e[0;35m\]$(__git_ps1 " (%s)")\[\e[0m\] \$ '
```

5) Colorful Prompt with Date and Time: This will display the date in red, time in green, username in yellow, hostname in blue, and current directory in blue.

```bash
PS1='\[\e[0;31m\]\d \[\e[0;32m\]\t \[\e[0;33m\]\u@\h \[\e[0;34m\]\w\[\e[0m\] \$ '
```

6) Minimal Prompt: This will display the username in green, hostname in green, and current directory in green.

```bash
PS1='\[\e[0;32m\]\u@\h:\w\[\e[0m\]$ '
```

7) Prompt with Exit Status: This will display the exit status of the last command in red, followed by the username in green, hostname in blue, and current directory in blue.

```bash
PS1='\[\e[0;31m\]$?\[\e[0m\] \[\e[0;32m\]\u@\h \[\e[0;34m\]\w\[\e[0m\] \$ '
```

8) Prompt with Shell Level: This will display the shell level in purple, followed by the username in green, hostname in blue, and current directory in blue.

```bash
PS1='\[\e[0;35m\]$SHLVL \[\e[0;32m\]\u@\h \[\e[0;34m\]\w\[\e[0m\] \$ '
```

9) to show the Git branch and have the prompt followed by a new line and the prompt symbol, This will display the username in green, hostname in blue, current directory in blue, current Git branch in purple, followed by a new line and the prompt symbol.

```bash
PS1='\[\e[0;32m\]\u@\h \[\e[0;34m\]\w\[\e[0;35m\]$(__git_ps1 " (%s)")\[\e[0m\]\n\[\033[00m\]\$ '
```

10) to display: The username in green, The hostname in blue., The current directory in blue, The current Git branch in purple., The current time (HH:MM:SS) in yellow., Followed by a new line and the prompt symbol.

```bash
PS1='\[\e[0;32m\]\u@\h \[\e[0;34m\]\w\[\e[0;35m\]$(__git_ps1 " (%s)") \[\e[0;33m\]\t\[\e[0m\]\n\[\033[00m\]\$ '
```
