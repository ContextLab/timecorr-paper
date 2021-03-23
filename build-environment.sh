#!/usr/bin/env bash
# build new environment from file
# it'll be named whatever you changed the first line of environment.yml to
conda env create -f environment.yml
# activate the environment so the remaining commands run inside it
conda activate timecorr_env_spotcheck

pip install git+git://github.com/lucywowen/timecorr-1.git@spot_check
pip install git+https://github.com/FIU-Neuro/brainconn.git

