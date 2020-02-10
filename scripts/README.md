## Hexfarm Developer Scripts (for HEXCMS Users at RU)

`hexfarm` source mirror on the Hexfarm available at: 

```bash
hexcms.rutgers.edu:/users/h2/bhgomes/docs/projects/hexfarm
```

---

To setup your `hexfarm` environment, run one or both of these scripts.


#### [`hexcms_setup.sh`](hexcms_setup.sh)

This script should be run first to install a conda environment in your home 
directory and to download the relevant packages from the Anaconda Cloud.

#### [`dev_setup.sh`](dev_setup.sh) 

For developers of `hexfarm` who want a separate environment, run this script 
to install the latest `hexfarm` environment with ROOT.

#### Temporary Setup

To install the `hexfarm` environment directly into your `base` environment use

```bash
conda env update -n base -f environment.yml
pip install hexfarm
```

This will not be needed when `hexfarm` has a completed conda build.
