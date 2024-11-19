import pandas as pd
import numpy as np
import argparse
import os
import sys
import subprocess

# GP2 Pathogenic Variant Analysis

# - **Project:** Parkinson’s Disease Pathogenic Variants: Cross-Ancestry Analysis and Microarray Data Validation
# - **Version:** Python/3.10.15
    
## Script Overview

# Helper script to extract pathogenic variants from SNP metrics via swarm for 01_extract_pathogenic_variants_snp_metrics.ipynb

## CHANGELOG

# 17-SEP-2024: Script started
# 19-NOV-2024: Script cleanup for publication


def shell_do(command, log=False, return_log=False):
    print(f'Executing: {(" ").join(command.split())}', file=sys.stderr)

    res=subprocess.run(command.split(), stdout=subprocess.PIPE)

    if log:
        print(res.stdout.decode('utf-8'))
    if return_log:
        return(res.stdout.decode('utf-8'))

if __name__ == '__main__':

    # argparse for chromosome specification
    parser = argparse.ArgumentParser(description='Metrics Parser')
    parser.add_argument('--chr', type=int, default=1, help='Chromosome to get metrics for')
    args = parser.parse_args()
    chrom = args.chr
    
    # data paths
    ## Note: using samples from release 6 since they are processed already
    ## This will not affect results since sample from release 6 are all included in release 7
    wd = '/path/to/working/directory'
    snp_metrics_data_dir = '/path/to/snp/metrics'
    master_key_full_path = '/path/to/full/master/key'
    master_key_release_path = f'/path/to/release6/master/key'
    genotype_path = '/path/to/release6/plink/genotypes'
    
    # read full master key and release master key
    master_key_full = pd.read_csv(master_key_full_path, sep='\t')
    master_key_full = master_key_full.rename({'filename':'IID'}, axis=1)
    master_key_release = pd.read_csv(master_key_release_path)
    
    # merge master keys and subset samples down to those included in the release
    master_key_merge = master_key_full[['GP2sampleID', 'IID', 'SentrixBarcode_A']].merge(master_key_release[['GP2sampleID', 'gp2_phenotype', 'label','pruned']], how='inner', on=['GP2sampleID'])
    master_key_merge = master_key_merge[master_key_merge['pruned'] == 0]
    
    # dictionaries and df for metrics and maf
    metrics_samples = {}
    full_bim_snps = pd.DataFrame()
    
    # loop through ancestires to initialize nested dictionaries
    for ancestry in master_key_merge['label'].unique():
        
        # only ancestries with >50 samples get metrics extracted
        if master_key_merge['label'].value_counts()[ancestry] > 50:
            bim = pd.read_csv(f'{genotype_path}.pvar', sep='\s+')
            bim = bim.rename({'ID':'snpID','POS':'bp'}, axis=1)
            
            # isolate chromosomes one by one according to the list in the hackathon_rv_extract_snp_metrics.ipynb notebook
            ## Note: positions on each chromosome are copied over from the hackathon_rv_extract_snp_metrics.ipynb notebook as well
            if chrom == 'M':
                bim = bim[bim['#CHROM'] == 'MT']
            elif chrom == 1:
                bim = bim[bim['#CHROM'] == 1]
                bim = bim[bim['bp'].isin([155235197, 155235205, 155235819, 155235843, 155236246, 155236420, 155237394, 155237412, 155237446, 155238141, 155238174, 155238214, 155238228, 155238258, 155238290, 155238291, 155238608, 155238631, 155239639, 155240025, 16986091, 16986235, 16986335, 16986490, 16986526, 16986554, 16986571, 16986610, 16986818, 16986847, 16988138, 16988161, 16988338, 16988444, 16988465, 16989977, 16990132, 16990133, 16990208, 16990254, 16990276, 16991787, 16991795, 16992019, 16992301, 16992322, 16992348, 16992378, 16992564, 16993667, 16993668, 16993690, 16996069, 16996255, 16996293, 16996298, 16996448, 16996487, 16996489, 16997087, 16997135, 16997136, 17000057, 17000099, 17000107, 17000307, 17000494, 17004773, 17005465, 17005548, 17005747, 17005753, 17011732, 20633615, 20633713, 20633815, 20633840, 20637868, 20637888, 20637956, 20638012, 20644540, 20644571, 20644649, 20645615, 20645665, 20645675, 20645695, 20648528, 20648534, 20648612, 20649224, 20650643, 20650673, 65392454, 7962868, 7984985])]
            elif chrom == 2:
                bim = bim[bim['#CHROM'] == 2]
                bim = bim[bim['bp'].isin([74530221, 74530396, 74531866, 74532634])]
            elif chrom == 3:
                bim = bim[bim['#CHROM'] == 3]
                bim = bim[bim['bp'].isin([132477995, 132494190])]
            elif chrom == 4:
                bim = bim[bim['#CHROM'] == 4]
                bim = bim[bim['bp'].isin([41261759, 89822254, 89822327, 89822336])]
            elif chrom == 6:
                bim = bim[bim['#CHROM'] == 6]
                bim = bim[bim['bp'].isin([161350125, 161350187, 161350208, 161360169, 161548937, 161569369, 161785829, 161785899, 161973317, 162201134, 162201143, 162262692, 162262763, 162443314, 162443356, 162443371, 162443383, 162443433])]
            elif chrom == 12:
                bim = bim[bim['#CHROM'] == 12]
                bim = bim[bim['bp'].isin([40225233, 40225580, 40235634, 40238078, 40240543, 40243668, 40249843, 40251273, 40251346, 40252958, 40257283, 40259507, 40259578, 40263791, 40263806, 40284011, 40293624, 40308476, 40308481, 40314043, 40320043, 40323256, 40328416, 40335008, 40340400, 40354304, 40356145, 40359345, 40363440, 40363526, 40364956])]
            elif chrom == 15:
                bim = bim[bim['#CHROM'] == 15]
                bim = bim[bim['bp'].isin([61856408, 61922492, 62012126, 62028419, 89316771, 89316804, 89316819, 89317379, 89317389, 89317407, 89317455, 89317460, 89317470, 89317500, 89317531, 89318553, 89318555, 89318573, 89318579, 89318587, 89318611, 89318640, 89318736, 89318737, 89318946, 89318962, 89318982, 89318985, 89318988, 89319006, 89319053, 89319065, 89319234, 89319257, 89319308, 89320850, 89320857, 89320867, 89320869, 89320877, 89320890, 89320894, 89320939, 89320948, 89321007, 89321135, 89321194, 89321217, 89321223, 89321239, 89321246, 89321258, 89321761, 89321770, 89321771, 89321793, 89321846, 89321847, 89322749, 89323405, 89323423, 89323449, 89323460, 89323462, 89323823, 89323851, 89323863, 89324126, 89324137, 89324149, 89324150, 89324156, 89324158, 89324194, 89324200, 89324221, 89325456, 89325470, 89325494, 89325494, 89325501, 89325512, 89325516, 89325519, 89325531, 89325549, 89325557, 89325562, 89325591, 89325609, 89325610, 89325619, 89325638, 89325656, 89325678, 89326695, 89326698, 89326725, 89326947, 89326952, 89327198, 89327211, 89327214, 89327244, 89327289, 89327300, 89327324, 89327325, 89327331, 89327349, 89328508, 89328532, 89328699, 89328789, 89328991, 89328996, 89328996, 89329011, 89329051, 89329055, 89329098, 89329104, 89330106, 89330133, 89330138, 89330257, 89330258, 89333152, 89333233, 89333239, 89333271, 89333327, 89333347, 89333364, 89333425, 89333427, 89333491, 89333491, 89333569, 89333601, 89333624, 89333626, 89333668])]
            elif chrom == 16:
                bim = bim[bim['#CHROM'] == 16]
                bim = bim[bim['bp'].isin([46660543, 46671809, 46674439, 46674616, 46679015])]
                
            # for whatever reason some chr 21 and 22 have string values in the release bim file
            elif chrom == 21:
                bim = bim[(bim['#CHROM'] == 21) | (bim['#CHROM'] == '21')]
                bim = bim[bim['bp'].isin([32639767, 32665968, 32666479, 32688306, 32726858])]
            elif chrom == 22:
                bim = bim[bim['#CHROM'] == '22']
                bim = bim[bim['bp'].isin([32479135, 32485115, 32491175, 32498467, 32498496, 32498507, 38112165, 38112212, 38112295, 38112521, 38112541, 38112558, 38112565, 38113560, 38113561, 38115578, 38115582, 38115663, 38116119, 38116155, 38116156, 38116176, 38120776, 38120886, 38120887, 38120888, 38123138, 38123185, 38123191, 38123251, 38126374, 38126390, 38128349, 38129529, 38132850, 38132917, 38132922, 38132942, 38132952, 38133010, 38135034, 38140006, 38143219, 38145447, 38145467, 38145477, 38145538, 38145597, 38145625, 38169218, 38169326])]
            
            else:
                bim = bim[bim['#CHROM'] == chrom]
        
            # setting metrics samples dictionary for each ancestry
            metrics_samples[ancestry] = {
                'count': master_key_merge['label'].value_counts()[ancestry],
                'PD': 0,
                'Control': 0,
                'snps': bim[['snpID']],
                'metrics': []
            }
    
            # getting full set of SNPs in bim files
            full_bim_snps = pd.concat([full_bim_snps, metrics_samples[ancestry]['snps']])
    
    # drop any duplicate snps between ancestires
    full_bim_snps = full_bim_snps.drop_duplicates(ignore_index=True)
    print(full_bim_snps.shape)
    
    # loop through barcodes
    for barcode in master_key_merge['SentrixBarcode_A'].unique():
        # check if barcode dir exists
        dir_path = f'{snp_metrics_data_dir}/{barcode}'
        parquet_path = f'{snp_metrics_data_dir}/{barcode}/snp_metrics_{barcode}'
        if os.path.isdir(dir_path) and os.path.isdir(parquet_path):
            # isolate samples from that barcode in master key
            master_key_merge_barcode = master_key_merge[master_key_merge['SentrixBarcode_A'] == barcode]
            
            # loop through samples
            for iid in master_key_merge_barcode['IID']:
                # ensure sample dir exists
                sample_path = f'{parquet_path}/Sample_ID={iid}'
                
                if os.path.isdir(sample_path):
                    # isolate specific sample from master key
                    sample = master_key_merge_barcode[master_key_merge_barcode['IID'] == iid]
                    
                    # ensure ancestry needs metrics
                    if sample['label'].values[0] in metrics_samples.keys():
                        # if there are less than 200 samples in an ancestry group take all of them
                        if metrics_samples[sample['label'].values[0]]['count'] < 200:
                            if (sample['gp2_phenotype'].values[0] == 'PD') | (sample['gp2_phenotype'].values[0] == 'Control'):
                                metrics_samples[sample['label'].values[0]][sample['gp2_phenotype'].values[0]] += 1
                                
                                metrics = pd.read_parquet(sample_path)
                                metrics = metrics[metrics['chromosome'] == str(chrom)]
    
                                metrics_needed = metrics[['snpID','R','Theta','GenTrain_Score','GT','chromosome','position']]
                                metrics_needed['Sample_ID'] = iid
    
                                metrics_needed = metrics_needed.merge(metrics_samples[sample['label'].values[0]]['snps'], how='inner', on=['snpID'])
                                metrics_needed['phenotype'] = sample['gp2_phenotype'].values[0]
    
                                metrics_samples[sample['label'].values[0]]['metrics'].append(metrics_needed)
    
                        # otherwise take up to 50 cases and 150 controls
                        else:
                            if (metrics_samples[sample['label'].values[0]]['PD'] < 50) & (sample['gp2_phenotype'].values[0] == 'PD'):
                                metrics_samples[sample['label'].values[0]]['PD'] += 1
                                
                                metrics = pd.read_parquet(sample_path)
                                metrics = metrics[metrics['chromosome'] == str(chrom)]
    
                                metrics_needed = metrics[['snpID','R','Theta','GenTrain_Score','GT','chromosome','position']]
                                metrics_needed['Sample_ID'] = iid
    
                                metrics_needed = metrics_needed.merge(metrics_samples[sample['label'].values[0]]['snps'], how='inner', on=['snpID'])
                                metrics_needed['phenotype'] = 'PD'
    
                                metrics_samples[sample['label'].values[0]]['metrics'].append(metrics_needed)
    
                            if (metrics_samples[sample['label'].values[0]]['Control'] < 150) & (sample['gp2_phenotype'].values[0] == 'Control'):
                                metrics_samples[sample['label'].values[0]]['Control'] += 1
                                
                                metrics = pd.read_parquet(sample_path)
                                metrics = metrics[metrics['chromosome'] == str(chrom)]
    
                                metrics_needed = metrics[['snpID','R','Theta','GenTrain_Score','GT','chromosome','position']]
                                metrics_needed['Sample_ID'] = iid
    
                                metrics_needed = metrics_needed.merge(metrics_samples[sample['label'].values[0]]['snps'], how='inner', on=['snpID'])
                                metrics_needed['phenotype'] = 'Control'
    
                                metrics_samples[sample['label'].values[0]]['metrics'].append(metrics_needed)
    
    # check if the metrics output dir exists and create it if not
    metrics_dir = f'/path/to/output/directory'
    if not os.path.isdir(metrics_dir):
        os.makedirs(metrics_dir)
    
    # loop through ancestires and check for/create ancestry-specific dirs
    for ancestry in metrics_samples:
        ancestry_dir = f'{metrics_dir}/{ancestry}'
        
        if not os.path.isdir(ancestry_dir):
            os.makedirs(ancestry_dir, exist_ok=True)
        
        # write sample metrics to file
        metrics_samples_ancestry = pd.concat(metrics_samples[ancestry]['metrics'], axis=0)
        metrics_samples_ancestry.to_csv(f'{ancestry_dir}/chr{chrom}_metrics.csv', sep=',', index=False)
