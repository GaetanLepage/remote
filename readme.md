[![PyPI - Python Version](https://badge.fury.io/py/labml-remote.svg)](https://badge.fury.io/py/labml-remote)
[![PyPI Status](https://pepy.tech/badge/labml_remote)](https://pepy.tech/project/labml_remote)
[![PyPI Status](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://join.slack.com/t/labforml/shared_invite/zt-egj9zvq9-Dl3hhZqobexgT7aVKnD14g/)

# 🕹 LabML Remote

![labml_remote job-list](https://github.com/lab-ml/remote/raw/master/notes/ddp-job-list.png)

`labml_remote` is a very simple tool that lets you setup python and
 run python programs on remote computers.
It's mainly intended for deep learning model training.
It simply connects to remote computers via SSH to run commands,
 and synchronises content using rsync.
 
`labml_remote` comes with a easy-to-use **Command-line Interface**.
You can also use the API to launch 
custom distributed training sessions.
[Here is an example](https://github.com/lab-ml/remote/blob/master/sample/api_sample.py).

### Install from PIP

```bash
pip install labml_remote
```

### Initialize and add server details

Go to your project folder.

```bash
cd [PROJECT]
```

Initialize for remote execution
```bash
labml_remote init
```

`labml_remote init` asks for your SSH credentials and creates two files `[PROJECT].remote/configs.yaml`
and `[PROJECT].remote/exclude.txt`.

`[PROJECT].remote/configs.yaml` keeps the remote configurations for the project.
Here's a sample `.remote/configs.yaml`:

```yaml
name: sample
servers:
  primary:
    hostname: 3.19.32.53
    private_key: ./.remote/private_key
  secondary:
    hostname: 3.19.32.54
```

Each of the servers can have the following attributes:

```yaml
hostname: [IP address of hostname]
private_key: [Location of the private key file; leave blank if not necessary]
username: [Username to SSH with; defaults to 'ubuntu']
password: [Password to connect with; leave blank if not necessary]
```

`.remote/exclude.txt` is like `.gitignore` - it specifies the files and folders that you dont need
to sync up with the remote server. The excludes generated by `labml_remote init` excludes
things like `.git`, `.remote`, `logs` and `__pycache__`.
You should edit this if you have things that you don't want to be synced 
with your remote computer.

See our [sample project](https://github.com/lab-ml/remote/tree/master/sample)  for a more complex example.

## 💻 CLI

Get the command line interface help with,

```bash
labml_remote --help
```

Use the flag `--help` with any command to get the help for that command.

### Prepare the servers

```bash
labml_remote prepare
```

This will install Conda on the servers, rsync your project content and install the
 Python packages based on your `requirements.txt` or `Pipfile`.

### Run a command

```bash
labml_remote run --cmd 'python my_script.py'
```

This will execute the command on the server and stream the output of it.

## 👩‍🔬 Jobs

Jobs are processes run with `nohup`.
These can run on the remote computers in background without streaming outputs over SSH.
The `stderr` and `stdout` of jobs will be piped to files and can be synchronized back to  the local computer using rsync.
`labml_remote` has commands to list, watch and kill jobs.

Jobs are intended to be used for tasks like model training.

### Start a new job

```bash
labml_remote job-run --cmd 'python my_script.py' --tag my-job
```

### List jobs

```bash
labml_remote job-list --rsync
```

`--rysnc` flag will sync up the job information from server to your local computer before
listing.

### Tail a job output

```bash
labml_remote job-tail --tag my-job
```

This will keep on tailing the output of the job.

### Kill jobs

```bash
labml_remote job-kill --tag my-job
```

### [Launch a PyTorch distributed training session](https://github.com/lab-ml/remote/blob/master/notes/pytorch-ddp.md)

```bash
labml_remote helper-torch-launch --cmd 'train.py' --nproc-per-node 2 --env GLOO_SOCKET_IFNAME enp1s0
```
Here `train.py` is the training script. We are using computers  with 2 GPUs, we want two processes per computer
so `--nproc-per-node` is 2. `--env GLOO_SOCKET_IFNAME enp1s0` sets environment variable `GLOO_SOCKET_IFNAME` to
`enp1s0`. You can specify multiple environment variables with `--env`.

## How it works

It sets up *miniconda* if it is not already installed and create a new environment for the project.
Then it creates a folder by the name of the project inside home folder and synchronises the contents
of your local folder with the remote computer.
It syncs using *rsync* so subsequent synchronisations only need to send the changes.
Then it installs packages from `requirements.txt` or with *pipenv* if a `Pipfile` is found.
It will use *pipenv* to run your commands if a `Pipfile` is present.
The outputs of commands are streamed backed to the local computer and the outputs of jobs redirected to
files on the server which are synchronized back to the local computer using *rsync*.

## What it doesn't do

This won't install things like drivers or CUDA. So if you need them you should pick an
image that comes with those for your instance. For example, on AWS pick a deep learning
AMI if you want to use an instance with GPUs.
