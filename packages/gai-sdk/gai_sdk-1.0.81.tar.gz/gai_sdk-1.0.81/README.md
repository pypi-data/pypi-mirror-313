# GAI SDK Setup Guide

## Install

1.  Clone Repository recursively

```bash
git clone https://github.com/kakkoii1337/gai-sdk --recursive
```

2. Update submodule branches

```bash
cd gai-sdk
git submodule foreach -q --recursive 'git checkout $(git config -f $toplevel/.gitmodules submodule.$name.branch || echo master)'
```

3.  Create conda env

```bash
conda create -n gai-sdk python=3.10.10 -y
conda activate gai-sdk
```

4.  Install Packages

```bash
poetry install
```

---

## Initialise

```bash
gai init
```

## Download model

```bash
gai pull exllamav2-mistral7b
```

## Start server

```
gai docker start
```

If it is successfully started, you will see the following:

```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:12031 (Press CTRL+C to quit)
```

## Test

```bash
gai news
```

![demo](./doc/img/gai-cli.gif)

## Quick Start

Run [Quick Start Guide](./doc/1-quickstart.ipynb)
