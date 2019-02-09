#!/bin/sh
# Hexfarm Setup Script

cd $HOME

wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

bash Miniconda3-latest-Linux-x86_64.sh
rm Miniconda3-latest-Linux-x86_64.sh

conda upgrade conda
conda install pip, root

pip install hexfarm

conda clean --all
