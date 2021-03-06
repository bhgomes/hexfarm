#!/bin/sh
# Hexfarm Setup Script

cd $HOME

wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
bash miniconda.sh -b -p $HOME/.miniconda
export PATH="$HOME/miniconda/bin:$PATH"
rm miniconda.sh

conda upgrade conda
conda config --add channels conda-forge
conda config --add channels rutgers
conda install git pip

pip install hexfarm
# TODO: change to `conda install hexfarm`

conda clean --all
