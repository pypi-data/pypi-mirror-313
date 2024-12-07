# MHCSeqNet

[![PyPI version](https://badge.fury.io/py/MHCSeqNet.svg)](https://badge.fury.io/py/MHCSeqNet)
[![Please Cite](https://zenodo.org/badge/doi/10.1186/s12859-019-2892-4.svg)](https://doi.org/10.1186/s12859-019-2892-4
)
[![Source code](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/natapol/kitsune)

## What is MHCSeqNet?

MHCSeqNet is a MHC ligand prediction python package developed by the [Computational Molecular Biology Group](http://cmb.md.chula.ac.th/) and [S3Bio Lab](http://s3bio.gitlab.io/) at Chulalongkorn University, Bangkok, Thailand. MHCSeqNet utilizes recurrent neural networks to process input ligand's and MHC allele's amino acid sequences and therefore can be to extended to handle peptide of any length and any MHC allele with known amino acid sequence. 

## version history

1.0: The model was trained using only data from MHC class I and supports peptides ranging from 8 to 15 amino acids in length, but the model can be re-trained to support more alleles and wider ranges of peptide length.

1.1.0: The package was update to the latest version of Tensorflow and only support for onehot model prediction

Please see our [Publication](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-019-2892-4) for more information.

### Models

MHCSeqNet offers two versions of prediction models

1. One-hot model: This model uses data from each MHC allele to train a separate predictor for that allele. The list of supported MHC alleles for the current release can be found [here](https://github.com/S3Bio/MHCSeqNet/blob/update/src/MHCSeqNet/PretrainedModels/onehot/supported_alleles.txt) 

2. Sequence-based model: This model use data from all MHC alleles to train a single predictor that can handle any MHC allele whose amino acid sequence is known. For more information on how our model learns MHC allele information in the form of amino acid sequence, please see our [Publication](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-019-2892-4). The list of MHC alleles used to train this model can be found [here](https://github.com/S3Bio/MHCSeqNet/blob/update/src/MHCSeqNet/PretrainedModels/sequence/supported_alleles.txt)

## How to install?
MHCSeqNet requires Python 3 (>= 3.8) and the following Python packages:

```
numpy
tensorflow (>= 2.10.0)
```
If your system has both Python 2 and Python 3, please ensure that Python 3 is used when following these instructions.
So that you know, we cannot promise whether MHCSeqNet will work with older versions of these packages.

### install packages

```{bash}
python -m pip install MHCSeqNet
```

### Install MHCSeqNet from the source

1. Clone this repository
```
git clone https://github.com/s3bio/MHCSeqNet
```
Or you may find other methods for cloning a GitHub repository [here](https://help.github.com/articles/cloning-a-repository/)

2. Install the latest version of 'pip' and 'setuptools' packages for Python 3 if your system does not already have them
```
python -m ensurepip --default-pip
pip install setuptools
```
If you have trouble with this step, more information can be found [here](https://packaging.python.org/tutorials/installing-packages/#install-pip-setuptools-and-wheel)

3. Run Setup.py inside the MHCSeqNet directory to install MHCSeqNet.
```
cd MHCSeqNet
python Setup.py install
```

## How to use MHCSeqNet?

MHCSeqNet can be launched through the MHCSeqNet script or by editing sample scripts explained below

```{bash}
$ MHCSeqNet -h

usage: MHCSeqNet [-h] [-p PATH] [-m {onehot,sequence}] [-i {paired,complete}] peptide_file allele_file output_file

positional arguments:
  peptide_file          should each contains only one column, without header row
  allele_file           should each contains only one column, without header row
  output_file

optional arguments:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  Specify the path to pre-trained model directory. This should be either the 'one_hot_model' or the 'sequence_model' directory located in 'PATH/PretrainedModels/' where PATH is where
                        MHCSeqNet was downloaded to
  -m {onehot,sequence}, --model {onehot,sequence}
                        Specify whether the one-hot model or sequence-based model will be used
  -i {paired,complete}, --input-mode {paired,complete}
                        Specify whether the prediction should be made for each pair of peptide and allele on the same row of each input file [paired] or for all combinations of peptides and alleles
                        [complete] Print this message

```

Sample peptide and MHC allele files can be found in the 'Samples' directory


### Input format
Peptide: The current release supports peptides of length 8 - 15 and does not accept ambiguous amino acids.

MHC allele: For alleles included in the training set (i.e. supported alleles listed in the [models]() section), the model requires the 'HLA-A\*XX:YY' format. 

To add new MHC alleles to the sequence-based model, the names and amino acid sequences of the new alleles must first be added to the [AlleleInformation.txt](https://github.com/S3Bio/MHCSeqNet/blob/update/src/MHCSeqNet/PretrainedModels/sequence/AlleleInformation.txt) and [supported_alleles.txt](https://github.com/S3Bio/MHCSeqNet/blob/update/src/MHCSeqNet/PretrainedModels/sequence/supported_alleles.txt
) in the sequence-based model's directory.

### Output
MHCSeqNet output binding probability ranging from 0.0 to 1.0 where 0.0 indicates an unlikely ligand and 1.0 indicates a likely ligand.

## How to re-train MHCSeqNet?
This feature and instruction will be added in the future
