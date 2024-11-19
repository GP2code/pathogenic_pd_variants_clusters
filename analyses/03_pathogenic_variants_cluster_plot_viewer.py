import os
import sys
import subprocess
import datetime
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

# GP2 Pathogenic Variant Analysis

# - **Project:** Parkinson’s Disease Pathogenic Variants: Cross-Ancestry Analysis and Microarray Data Validation
# - **Version:** Python/3.10.15
    
## Script Overview

# Script to build pathogenic variant cluster plot viewer streamlit app using SNP metrics extracted in
# 01_extract_pathogenic_variants_snp_metrics.py and save all pathogenic variant plots to PNG

## CHANGELOG

# 9-OCT-2024: Script started
# 19-NOV-2024: Script cleanup for publication

# cluster plot function
def plot_clusters(df, x_col='theta', y_col='r', gtype_col='gt', title='snp plot'):
    d3 = px.colors.qualitative.D3

    cmap = {
        'AA': d3[0],
        'AB': d3[1],
        'BA': d3[1],
        'BB': d3[2],
        'NC': d3[3]
    }

    # custom limits to make plots look good for publication
    xlim = [0-.2, 1.2]
    ylim = [0-.1, 2.6]

    lmap = {'r':'R','theta':'Theta'}
    smap = {'Control':'circle','PD':'diamond-open-dot'}

    # plot and update axes for aesthetics
    fig = px.scatter(df, x=x_col, y=y_col, color=gtype_col, color_discrete_map=cmap, width=650, height=497, labels=lmap, symbol='phenotype', symbol_map=smap)

    fig.update_xaxes(range=xlim, nticks=10, zeroline=False)
    fig.update_yaxes(range=ylim, nticks=10, zeroline=False)
    
    fig.update_layout(margin=dict(r=76, t=63, b=75))


    fig.update_layout(legend_title_text='Genotype')

    out_dict = {
        'fig': fig,
        'xlim': xlim,
        'ylim': ylim
    }
    
    fig.update_layout(title_text=f'<b>{title}<b>')
    
    return out_dict

# callback function for cluster plot SNP selector
def snp_callback():
    st.session_state['old_snp_choice'] = st.session_state['snp_choice']
    st.session_state['snp_choice'] = st.session_state['new_snp_choice']

if __name__ == '__main__':
    # SNPs and metric path
    snp_metrics_path = f'data/updated_hackathon_snp_metrics.txt'
    pathogenic_snps_path = f'data/annotated_pathogenic_vars.txt'

    # read metrics into session state to cut down on load time and create merge id
    if 'snp_metrics' not in st.session_state:
        snp_metrics = pd.read_csv(snp_metrics_path, sep='\t')
        snp_metrics['merge_id'] = 'chr' + snp_metrics['chromosome'].astype(str) + ':' + snp_metrics['position'].astype(str) + ':' + snp_metrics['a2'] + ':' + snp_metrics['a1']
        snp_metrics['merge_id2'] = 'chr' + snp_metrics['chromosome'].astype(str) + ':' + snp_metrics['position'].astype(str) + ':' + snp_metrics['a1'] + ':' + snp_metrics['a2']
        st.session_state['snp_metrics'] = snp_metrics
    else:
        snp_metrics = st.session_state['snp_metrics']
    
    st.markdown(snp_metrics.shape)

    # read pathogenic snps and create merge id
    pathogenic_snps = pd.read_csv(pathogenic_snps_path, sep='\t')
    # pathogenic_snps[['chr','pos','alt','ref']] = pathogenic_snps['SNP'].str.split(':', expand=True)
    # pathogenic_snps['merge_id'] =  pathogenic_snps['Chr'].astype(str) + ':' + pathogenic_snps['Start'].astype(str)
    pathogenic_snps['merge_id'] = pathogenic_snps['Chr'].astype(str) + ':' + pathogenic_snps['Start'].astype(str) + ':' + pathogenic_snps['Ref'] + ':' + pathogenic_snps['Alt']
    st.markdown(pathogenic_snps.shape)
    

    # merge metrics with path snps
    path_metrics1 = snp_metrics.merge(pathogenic_snps, how='inner', on=['merge_id'])
    path_metrics1 = path_metrics1.drop_duplicates()
    st.markdown(path_metrics1.shape)
    st.markdown(len(path_metrics1['merge_id'].unique()))

    path_metrics2 = snp_metrics.merge(pathogenic_snps, how='inner', left_on=['merge_id2'], right_on=['merge_id'])
    path_metrics2 = path_metrics2.drop(columns=['merge_id_x', 'merge_id_y'], axis=1)
    path_metrics2 = path_metrics2.rename(columns={'merge_id2':'merge_id'})
    path_metrics2 = path_metrics2.drop_duplicates()
    st.markdown(path_metrics2.shape)
    st.markdown(len(path_metrics2['merge_id'].unique()))

    path_metrics = pd.concat([path_metrics1, path_metrics2], axis=0)
    st.markdown(path_metrics.shape)
    st.markdown(len(path_metrics['merge_id'].unique()))

    
    # set title
    st.title('Cluster Plot Browser')

    # get SNP options
    snp_options = ['Select SNP!']+[snp for snp in path_metrics['merge_id'].unique()]

    # set default SNP
    if 'snp_choice' not in st.session_state:
        st.session_state['snp_choice'] = snp_options[0]
    if 'old_snp_choice' not in st.session_state:
        st.session_state['old_snp_choice'] = ""

    # check if SNP choice is in the options
    ## Note: this was more of a concern for the full cohort browser, shouldn't happen anymore
    if st.session_state['snp_choice'] in snp_options:
        index = snp_options.index(st.session_state['snp_choice'])

    if st.session_state['snp_choice'] not in snp_options:
        if ((st.session_state['snp_choice'] != 'Select SNP!') and (int(st.session_state['snp_choice'].split('(')[1].split(':')[0]) == st.session_state['old_chr_choice'])):
            index = 0

    # SNP selector
    st.markdown('### Select SNP for Cluster Plot')
    st.session_state['snp_choice'] = st.selectbox(label='SNP', label_visibility='collapsed', options=snp_options, index=index, key='new_snp_choice', on_change=snp_callback)

    # if a SNP is selected, plot and output a table of the genotype value counts
    if st.session_state['snp_choice'] != 'Select SNP!':
        snp_df = path_metrics[path_metrics['merge_id'] == st.session_state['snp_choice']]
        snp_df = snp_df.reset_index(drop=True)

        fig = plot_clusters(snp_df, x_col='Theta', y_col='R', gtype_col='GT', title=st.session_state['snp_choice'])['fig']
        st.plotly_chart(fig, use_container_width=True)

        st.table(snp_df['GT'].value_counts())

    ## For plotting all SNPs ##
    for snp in snp_options:
        if snp != 'Select SNP!':
            snp_df = path_metrics[path_metrics['merge_id'] == snp]
            snp_df = snp_df.reset_index(drop=True)

            fig = plot_clusters(snp_df, x_col='Theta', y_col='R', gtype_col='GT', title=snp)['fig']
            fig.write_image(f"plots/{snp}.png")
