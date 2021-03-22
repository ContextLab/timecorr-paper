# What is the neural code?

This repository contains data and code used to produce the paper [_High-level cognition during story listening is reflected in high-order dynamic correlations in neural activity patterns_](https://www.biorxiv.org/content/10.1101/763821v1) by Lucy L.W. Owen, Thomas H. Chang, and Jeremy R. Manning.  You may also be interested in our [timecorr](https://timecorr.readthedocs.io/en/latest/) Python toolbox for calculating high-order dynamic correlations in timeseries data; the methods implemented in our timecorr toolbox feature prominently in our paper.

This repository is organized as follows:

```
root
└── code : all code used in the paper
    ├── notebooks : jupyter notebooks for paper analyses and instructions for downloading the data
    └── scripts : python scripts used to run analyses on a computing cluster
    └── figs : pdf and png copies of figures
└── data : create this folder by extracting the following zip archive into your clone of this repository's folder: https://drive.google.com/file/d/1CZYe8eyAkZFuLqfwwlKoeijgkjdW6vFs
└── paper : all files to generate paper
    └── figs : pdf copies of each figure
```

Content of the data folder is provided [here](https://drive.google.com/file/d/1CZYe8eyAkZFuLqfwwlKoeijgkjdW6vFs/view?usp=sharing).
We also include a Dockerfile to reproduce our computational environment. Instruction for use are below (copied and modified from [MIND](https://github.com/Summer-MIND/mind-tools) repo):

## Conda env setup
1. 
 
 
## Docker setup
1. Install Docker on your computer using the appropriate guide below:
    - [OSX](https://docs.docker.com/docker-for-mac/install/#download-docker-for-mac)
    - [Windows](https://docs.docker.com/docker-for-windows/install/)
    - [Ubuntu](https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/)
    - [Debian](https://docs.docker.com/engine/installation/linux/docker-ce/debian/)
2. Launch Docker and adjust the preferences to allocate sufficient resources (e.g. > 4GB RAM)
3. Build the docker image by opening a terminal in this repo folder and enter `docker build -t timecorr_paper .`  
4. Use the image to create a new container for the workshop
    - The command below will create a new container that will map your computer's `Desktop` to `/mnt` within the container, so that location is shared between your host OS and the container. Feel free to change `Desktop` to whatever folder you prefer to share instead, but make sure to provide the full path. The command will also share port `9999` with your host computer so any jupyter notebooks launched from *within* the container will be accessible at `localhost:9999` in your web browser
    - `docker run -it -p 9999:9999 --name Timecorr_paper -v ~/Desktop:/mnt timecorr_paper `
    - You should now see the `root@` prefix in your terminal, if so you've successfully created a container and are running a shell from *inside*!
5. To launch any of the notebooks: `jupyter notebook --port=9999 --no-browser --ip=0.0.0.0 --allow-root`

## Using the container after setup
1. You can always fire up the container by typing the following into a terminal
    - `docker start Timecorr_paper && docker attach Timecorr_paper`
    - When you see the `root@` prefix, letting you know you're inside the container
2. Close a running container with `ctrl + d` from the same terminal you used to launch the container, or `docker stop Timecorr_paper` from any other terminal

