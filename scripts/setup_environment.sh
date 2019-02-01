#!/bin/sh

cd $HOME

sh -c "$(curl -fsSL https://raw.githubusercontent.com/Linuxbrew/install/master/install.sh)"

mv .linuxbrew cmslink/.linuxbrew
mv .cache cmslink/.cache

# this should already be in your bashrc
export PATH="$HOME/cmslink/.linuxbrew/bin:$HOME/cmslink/.linuxbrew/sbin:$PATH"

brew vendor-install ruby

HOMEBREW_NO_AUTO_UPDATE=1 HOMEBREW_BUILD_FROM_SOURCE=1 brew install gcc --without-glibc
HOMEBREW_NO_AUTO_UPDATE=1 brew install glibc
HOMEBREW_NO_AUTO_UPDATE=1 brew remove gcc
HOMEBREW_NO_AUTO_UPDATE=1 brew install gcc

brew upgrade

brew install gcc@7
brew install cmake
brew install python3
brew install htop tree pipenv ipython node

cp /users/h2/bhgomes/extern/Miniconda3-latest-Linux-x86_64.sh $HOME/

# when it asks you if you want to change the path type:
#    /users/h2/ag1378/cmslink/.miniconda3
bash Miniconda3-latest-Linux-x86_64.sh

rm Miniconda3-latest-Linux-x86_64.sh

conda upgrade conda
conda install anaconda conda-build
conda config --add channels conda-forge bhgomes
conda install root geant4 pythia8
