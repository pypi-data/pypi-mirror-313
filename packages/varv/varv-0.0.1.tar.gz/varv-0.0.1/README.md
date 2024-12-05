# VarV

Code repository for Thijn's MEP.

The goal of this project is to implement variable voltage in the nanopore measurement for DNA-peptide conjugate translocation.

- LabView
- ...

```
cd existing_repo
git remote add origin https://gitlab.tudelft.nl/xiuqichen/varv.git
git branch -M main
git push -uf origin main
```

## Install

```shell
pip install varv
```

For Jupyter interactivity
```shell 
pip install varv[jupyter]
```

## Develop

Cloning the repository
```shell
git clone https://gitlab.tudelft.nl/xiuqichen/varv.git
cd varv
```

Creating a virtual environment for the Python packages
```shell
python -m venv .venv
```

Activating the virtual environment
```shell
source .venv/bin/activate
```

Install an editable version of the package
```shell
pip install -e .
```


## Test


