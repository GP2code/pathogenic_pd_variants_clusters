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
└── analyses
    ├── pathogenic_vars
    │   └── 00_Pathogenic_Variants_Analyses.ipynb
    └── cluster_plots
        ├── cluster_plot_metrics.py
        ├── cluster_plots.py
        ├── 00_hackathon_rv_extract_snp_metrics.ipynb
        └── requirements.txt
```
---
### Analyses Notebooks
* Languages: Python, bash

| **Directory** | File        | Description                        |
|---------------|------------------|------------------------------------|
| pathogenic_vars/   | 00_Pathogenic_Variants_Analyses | Running pathogneic variant annotations and calculating frequencies |
| cluster_plots/          | cluster_plots_metrics | x |
|           | cluster_plots | x |
|           | 00_hackathon_rv_extract_snp_metrics | x |

---

# Software
|               Software              |  Version(s) |                              Resource URL                              |       RRID      |                                               Notes                                               |
|:-----------------------------------:|:-----------:|:----------------------------------------------------------------------:|:---------------:|:-------------------------------------------------------------------------------------------------:|
|     Python Programming Language     | 3.10 |                         http://www.python.org/                         | RRID:SCR_008394 | pandas; numpy |
|                PLINK                |     1.9 and 2.0     |                   http://www.nitrc.org/projects/plink                  | RRID:SCR_001757 |                                     used for genetic analyses                                     |
|    ANNOVAR    | version 2020-06-07 | http://www.openbioinformatics.org/annovar/ | RRID:SCR_012821 | refGene; avsnp151; clinvar_20240917; dbnsfp33a |
