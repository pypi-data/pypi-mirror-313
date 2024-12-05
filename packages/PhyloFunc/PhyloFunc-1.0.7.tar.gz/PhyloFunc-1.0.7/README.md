# PhyloFunc

'PhyloFunc' is a Python package for generating PhyloFunc to incorporate microbiome phylogeny to inform on metaproteomic functional distance. 
It enables efficient calculation of functional beta-diversity distances between sample pairs and generates comprehensive distance metrics across multiple samples.

## Installation of package

You can install this package via pip:  
pip install PhyloFunc

## Usage
Once installed, you can use the PhyloFunc package in a Python script or an interactive environment.

### Quick Start

#### Import package

from PhyloFunc import PhyloFunc_distance  
from PhyloFunc import PhyloFunc_matrix

#### Script
Two input parameters are required. The first is a phylogenetic tree (default: bac120_iqtree_v2.0.1.nwk). The second is a phylogeny-informed Taxon-Function table, which includes columns labeled Taxon, Function, and the names of samples (default: Taxon_Function_distance.csvor Taxon_Function_matrix.csv).

#### 1. Calculate PhyloFunc distance between sample pairs
PhyloFunc_distance(tree_file='bac120_iqtree_v2.0.1.nwk', sample_file='Taxon_Function_distance.csv')

#### 2. Calculate PhyloFunc distance matrix across multiple samples
PhyloFunc_matrix(tree_file='bac120_iqtree_v2.0.1.nwk', sample_file='Taxon_Function_matrix.csv')

### Output
PhyloFunc distance or PhyloFunc distance matrix can be output.

## Performance optimization
This package improves performance by reducing disk I/O operations and processing data in memory. This enables faster computations with large datasets.

## Project structure
```
PhyloFunc/  
├── __init__.py  
├── PhyloFunc.py  
│  └── The main function code.  
├── data/  
│  ├── Taxon_Function_distance.csv
│  │  └── Data file for calculating the distance between two samples. 
│  ├── Taxon_Function_matrix.csv
│  │  └── Data file for calculating distances matrix across multiple samples.  
│  └── bac120_iqtree_v2.0.1.nwk  
│     └── Phylogenetic tree file.  
└── PhyloFunc_Package_Tutorial.ipynb
   └── Demonstrates the specific application of this package.
```

## Contribution
Welcome code contributions and improvement suggestions! Feel free to submit an issue or a pull request on GitHub.

## License
This project uses an MIT license. For details, see the LICENSE file.

## Application
For more detailed usage instructions, please refer to the paper：
Wang and Li et al., PhyloFunc: Phylogeny-informed Functional Distance as a New Ecological Metric for Metaproteomic Data Analysis
doi: https://doi.org/10.1101/2024.05.28.596184