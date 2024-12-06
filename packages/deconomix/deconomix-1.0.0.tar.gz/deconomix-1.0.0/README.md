# Deconomix

## Overview

Deconomix is a Python library aimed at the bioinformatics community, offering methods to estimate cell type compositions, hidden background contributions and gene regulation factors of bulk RNA mixtures. Visit the documentation [here](https://medbioinf.pages.gwdg.de/MedicalDataScience/DeconomiX/).

## Features

- **Data Simulation**: Generate artificial bulk mixtures from single-cell data in an efficient way to provide training data for your models.

- **Gene Weighting**: Learn gene weights from artifical bulk mixtures to optimize the cellular composition estimation of real bulk RNA mixtures.

- **Cellular Composition**: Estimate the cellular composition of your bulk RNA profiles or Spatial Transcriptomics spots.

- **Background Estimation**: Refine the composition estimation by estimate a hidden background contribution and profile, which cannot be explained by the cell types featured in the reference.

- **Gene Regulation**: Find out, how cell types in your bulk data is regulated in relation to your reference profiles, for instance in a disease context.

- **Visualization**: Visualize your results with predefined functions.

- **Evaluation**: Perform basic enrichment analysis for the estimated gene regulatory factors.



## Installation

You can install the package using `pip`:
```
pip install deconomix
```

Or directly from the `git` repository:
```
pip install git+https://gitlab.gwdg.de/MedBioinf/MedicalDataScience/DeconomiX.git
```



## Getting Started
For a detailed showcase of the standard workflow please visit our [gitlab page](https://gitlab.gwdg.de/MedBioinf/MedicalDataScience/DeconomiX) and navigate to the example folder. There we provide a jupyter notebook with all neccesary steps to get started. We also encourage the user to take a look at our [documentation](https://medbioinf.pages.gwdg.de/MedicalDataScience/DeconomiX/).


## Publications
Görtler, F. et al. (2020). Loss-Function Learning for Digital Tissue Deconvolution. Journal of Computational Biology, 27(3), 342–355.
Görtler, F. et al. (2024). Adaptive digital tissue deconvolution. Bioinformatics, 40(Supplement 1), i100–i109
Mensching-Buhr, M. and Sterr T. et al. (2024) bioRxiv 2024.11.28.625894; doi: https://doi.org/10.1101/2024.11.28.625894 (Preprint)
