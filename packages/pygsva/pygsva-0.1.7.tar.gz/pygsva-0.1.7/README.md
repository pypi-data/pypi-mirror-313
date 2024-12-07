
# pyGSVA: Gene Set Variation Analysis in Python

Gene Set Variation Analysis (GSVA) is a powerful gene set enrichment method designed for single-sample analysis. It enables pathway-centric analyses of molecular data by shifting the functional unit of analysis from individual genes to gene sets. This approach is particularly useful for bulk microarray, RNA-seq, and other molecular profiling data types, providing a pathway-level view of biological activity.

## Overview

GSVA transforms an input gene-by-sample expression data matrix into a gene-set-by-sample expression data matrix, representing pathway activities. This transformed data can then be utilized with classical analytical methods such as:

- **Differential Expression**
- **Classification**
- **Survival Analysis**
- **Clustering**
- **Correlation Analysis**

Additionally, GSVA enables pathway comparisons with other molecular data types, such as microRNA expression, binding data, copy-number variation (CNV), or single nucleotide polymorphisms (SNPs).

## Methods

The `pyGSVA` package provides Python implementations of four single-sample gene set enrichment methods:

### 1. **PLAGE** (Pathway Level Analysis of Gene Expression)
   - **Reference**: Tomfohr, Lu, and Kepler (2005)
   - Standardizes expression profiles over the samples.
   - Performs Singular Value Decomposition (SVD) on each gene set.
   - The coefficients of the first right-singular vector are returned as pathway activity estimates.
   - **Note**: The sign of singular vectors is arbitrary due to the nature of SVD.

### 2. **Z-Score Method**
   - **Reference**: Lee et al. (2008)
   - Standardizes expression profiles over the samples.
   - Combines standardized values for each gene in a gene set using the formula:
     \[
     Z_\gamma = rac{\sum_{i=1}^{k} z_i}{\sqrt{k}}
     \]
     where \( z_i \) are the standardized values of genes in a specific sample, and \( \gamma \) is the gene set.

### 3. **ssGSEA** (Single-Sample Gene Set Enrichment Analysis)
   - **Reference**: Barbie et al. (2009)
   - Calculates enrichment scores as the normalized difference in empirical cumulative distribution functions (CDFs) of gene expression ranks inside and outside the gene set.
   - By default, the pathway scores are normalized by dividing them by the range of calculated values. This normalization can be switched off.

### 4. **GSVA** (Default Method)
   - **Reference**: Hänzelmann, Castelo, and Guinney (2013)
   - A non-parametric method using empirical CDFs of gene expression ranks inside and outside the gene set.
   - Calculates an expression-level statistic to bring gene expression profiles with varying dynamic ranges to a common scale.

## Applications

- Estimate pathway activity for individual samples.
- Integrate pathway activity scores with traditional statistical analyses.
- Compare pathway activity across different molecular data types.

## Installation

```bash
git clone https://github.com/guokai8/pygsva
cd pygsva
python setup.py install --user
```

## Usage

```python
from pygsva import *

# Example usage with default GSVA method
hsko = load_hsko_data()
pbmc = load_pbmc_data()
gene_sets = {key: group.iloc[:, 0].tolist() for key, group in hsko.groupby(hsko.iloc[:, 2])}
##ssgsea
params=ssgseaParam(pbmc,gene_sets=gene_sets,remove_constant=False,remove_nz_constant=False,use_sparse=True)
res=ssgsea(pbmc,gene_sets,use_sparse=True,remove_constant=False,remove_nz_constant=False)
##gsva
param=gsvaParam(pbmc,gene_sets=gene_sets,use_sparse=True,kcdf="Poisson",n_jobs=1)
res=gsva(param)
##plage
paramp=plageParam(pbmc,gene_sets=gene_sets,use_sparse=True,min_size=2)
res=gsva(paramp)
##zscore
paramz=zscoreParam(pbmc,gene_sets,use_sparse=True)
res=gsva(paramz)
```

## References

If you use any of the methods in this package, please cite the corresponding articles:

1. Tomfohr, Lu, and Kepler (2005) - Pathway Level Analysis of Gene Expression (PLAGE)
2. Lee et al. (2008) - Z-Score Method
3. Barbie et al. (2009) - Single Sample Gene Set Enrichment Analysis (ssGSEA)
4. Hänzelmann, Castelo, and Guinney (2013) - Gene Set Variation Analysis (GSVA)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions please contact guokai8@gmail.com or https://github.com/guokai8/pygsva/issues
