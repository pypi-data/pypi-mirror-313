# Iker's Python Common Module

## Build and Deploy

### Using Conda

We recommend using Conda. You need to install Anaconda packages from
the [official site](https://www.anaconda.com/products/distribution)

Create a Conda environment and install the modules and their dependencies in it

```shell
conda create -n iker python=3.12
conda activate iker

pip install .

conda deactivate
```

To remove the existing Conda environment (and create a brand new one)

```shell
conda env remove -n iker
```
