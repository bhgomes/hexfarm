#!/bin/sh
# Hexfarm Development Setup

conda env update -f environment.yml --prune
conda env update -n hexfarm -f root-environment.yml
conda activate hexfarm
