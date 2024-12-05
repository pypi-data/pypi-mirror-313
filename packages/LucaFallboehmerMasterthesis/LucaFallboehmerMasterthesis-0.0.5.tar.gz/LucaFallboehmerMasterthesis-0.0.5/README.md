# masterthesis

This code was developed for my masterthesis in astroparticlephysics about **sterile neutrino search with neural networks** in the tritium $\beta$-decay spectrum.
It is currently maintained and still WIP.

# Disclaimer

The neural networks are based on the PyTorch Library.
For network training, the Nvidia CUDA backend as well as the Apple MPS backend were successfully tested and used.
Currently, the networks can only perform binary classification of an input spectrum. 
Sterile neutrino parameters (mass, active-to-sterile mixing angle) can currently not be inferred directly.

The response matrices used for sections of the analysis are from the TRModel version 2.

# Usage

In a nutshell, this library can do the following:
- Generate and modify $\beta$-spectra
- Train different kinds of Neural Networks for classification of $\beta$-spectra
- Evaluate Neural Networks regarding their sensitivity to a sterile neutrino signature

## Examples

A front to back showcase of everything this library is capable of can be found in masterthesis/notebooks/Cookbook.ipynb

Especially recommended is the google colab version of this notebook. (LINK)

## How to install

### Google Colab:

```
!pip install git+https://github.com/lucafally/masterthesis.git
```

Or to clone the repository (also possible in colab):

```
!git clone https://github.com/lucafally/masterthesis.git
```

Them simply run one of the available jupyter notebooks.
