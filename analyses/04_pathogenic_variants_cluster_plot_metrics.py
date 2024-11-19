import pandas as pd

# GP2 Pathogenic Variant Analysis

# - **Project:** Parkinson’s Disease Pathogenic Variants: Cross-Ancestry Analysis and Microarray Data Validation
# - **Version:** Python/3.10.15
    
## Script Overview

# Script to calculate metrics from analyset-scored cluster plots generated in 03_pathogenic_variants_cluster_plot_viewer.py

## CHANGELOG

# 2-NOV-2024: Script started
# 19-NOV-2024: Script cleanup for publication


if __name__ == '__main__':
    metrics_path = 'data/cluster_plot_metrics.csv'

    metrics = pd.read_csv(metrics_path, sep=',')
    print(metrics.head())

    for classification in metrics['Classification'].unique():
        metrics_class = metrics[metrics['Classification'] == classification]
        print(f'{classification} Shape')
        print(metrics_class.shape)
        print()

        print(f'{classification} NC Metrics')
        print(metrics_class['Number of NC'].mean())
        print(metrics_class['Number of NC'].min())
        print(metrics_class['Number of NC'].max())
        print()

        print(f'{classification} Missingness')
        print(metrics_class['GP2 r7 Missingness Rate'].mean())
        print()

        print(f'{classification} MAF')
        print(metrics_class['GP2 r7 MAF'].mean())
        print()


