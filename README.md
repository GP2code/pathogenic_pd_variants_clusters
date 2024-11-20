# Parkinson’s Disease Pathogenic Variants: Cross-Ancestry Analysis and Microarray Data Validation

**Last Updated:** November 2024 

## Summary
This is the online repository for the short report titled ***"Parkinson’s Disease Pathogenic Variants: Cross-Ancestry Analysis and Microarray Data Validation"***. This study aims to evaluate the genotyping success of the NeuroBooster array (NBA) and determine the frequencies of pathogenic variants across ancestries.

### Data Statement
* Data (DOI 10.5281/zenodo.10962119; release 7) used in the preparation of this article were obtained from the Global Parkinson’s Genetics Program (GP2).

### HelpfulLinks
- [GP2 Website](https://gp2.org/)
    - [GP2 Cohort Dashboard](https://gp2.org/cohort-dashboard-advanced/)
- [Introduction to GP2](https://movementdisorders.onlinelibrary.wiley.com/doi/10.1002/mds.28494)
    - [Other GP2 Manuscripts (PubMed)](https://pubmed.ncbi.nlm.nih.gov/?term=%22global+parkinson%27s+genetics+program%22)
    
# Repository Orientation
- The `analyses/` directory includes all analyses discussed in the manuscript

```
THIS_REPO
├── README.md
├── analyses 
│   ├── 00_pathogenic_variants_analyses.ipynb
│   ├── 01_extract_pathogenic_variants_snp_metrics.ipynb
│   ├── 02_extract_pathogenic_variants_snp_metrics.py
│   ├── 03_pathogenic_variants_cluster_plot_viewer.py
│   ├── 04_pathogenic_variants_cluster_plot_metrics.py
│   └── requirements.txt
├── plots
│   └── PNG files for all NBA-genotyped pathogenic variant cluster plots
└── output
    └── placeholder directory to read in files created in 00_pathogenic_variants_analyses.ipynb and 01_extract_pathogenic_variants_snp_metrics.ipynb into 03_pathogenic_variants_cluster_plot_viewer.py
```
---
### Analyses Notebooks
* Languages: Python, bash

| **Directory** | File        | Description                        |
|---------------|------------------|------------------------------------|
| analyses/   | 00_pathogenic_variants_analyses.ipynb | Running pathogenic variant annotations and calculating frequencies |
|             | 01_extract_pathogenic_variants_snp_metrics.ipynb | Extract pathogenic variant SNP metrics from full GP2 SNP metrics |
|             | 02_extract_pathogenic_variants_snp_metrics.py | Helper Python script to extract pathogenic variant SNP metrics from full GP2 SNP metrics in batch jobs |
|             | 03_pathogenic_variants_cluster_plot_viewer.py | Streamlit script to browse pathogenic variant cluster plots |
|             | 04_pathogenic_variants_cluster_plot_viewer.py | Helper python script to calculate pathogenic variant cluster plot metrics |
|             | requirements.txt | Required Python packages for 03_pathogenic_variants_cluster_plot_viewer.py |
| plots/   | *.png | PNG files for all NBA-genotyped pathogenic variant cluster plots |

---

# Software
|               Software              |  Version(s) |                              Resource URL                              |       RRID      |                                               Notes                                               |
|:-----------------------------------:|:-----------:|:----------------------------------------------------------------------:|:---------------:|:-------------------------------------------------------------------------------------------------:|
|     Python Programming Language     | 3.10 |                         http://www.python.org/                         | RRID:SCR_008394 | pandas; numpy |
|                PLINK                |     1.9 and 2.0     |                   http://www.nitrc.org/projects/plink                  | RRID:SCR_001757 |                                     used for genetic analyses                                     |
|    ANNOVAR    | version 2020-06-07 | http://www.openbioinformatics.org/annovar/ | RRID:SCR_012821 | refGene; avsnp151; clinvar_20240917; dbnsfp33a |
