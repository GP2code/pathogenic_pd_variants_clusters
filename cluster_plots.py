import os
import sys
import subprocess
import datetime
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

# snp metrics chromosome callback for session state
def chr_callback():
    st.session_state['old_chr_choice'] = st.session_state['chr_choice']
    st.session_state['chr_choice'] = st.session_state['new_chr_choice']

# snp metrics ancestry callback for session state
def ancestry_callback():
    st.session_state['old_ancestry_choice'] = st.session_state['ancestry_choice']
    st.session_state['ancestry_choice'] = st.session_state['new_ancestry_choice']

def chr_ancestry_select():
    st.sidebar.markdown('### **Choose a chromosome!**', unsafe_allow_html=True)

    # set chromosome options
    chr_options=[i for i in range(1,23)]

    # set default chromosome
    if 'chr_choice' not in st.session_state:
        st.session_state['chr_choice'] = chr_options[0]
    if 'old_chr_choice' not in st.session_state:
        st.session_state['old_chr_choice'] = ""

    # dynamic change of chromosome with selector
    st.session_state['chr_choice'] = st.sidebar.selectbox(label = 'Chromosome Selection', label_visibility = 'collapsed', options=chr_options, index=chr_options.index(st.session_state['chr_choice']), key='new_chr_choice', on_change=chr_callback)

    st.sidebar.markdown('### **Choose an Ancestry!**', unsafe_allow_html=True)

    # set ancestry options
    ancestry_options=['AAC','AFR','AJ','AMR','CAH','CAS','EAS','EUR','FIN','MDE','SAS']

    # set default ancestry
    if 'ancestry_choice' not in st.session_state:
        st.session_state['ancestry_choice'] = ancestry_options[0]
    if 'old_ancestry_choice' not in st.session_state:
        st.session_state['old_ancestry_choice'] = ""

    # dynamic change of ancestry with selector
    st.session_state['ancestry_choice'] = st.sidebar.selectbox(label = 'Ancestry Selection', label_visibility = 'collapsed', options=ancestry_options, index=ancestry_options.index(st.session_state['ancestry_choice']), key='new_ancestry_choice', on_change=ancestry_callback)

def plot_clusters(df, x_col='theta', y_col='r', gtype_col='gt', title='snp plot'):
    d3 = px.colors.qualitative.D3

    cmap = {
        'AA': d3[0],
        'AB': d3[1],
        'BA': d3[1],
        'BB': d3[2],
        'NC': d3[3]
    }

    # gtypes_list = (df[gtype_col].unique())
    # xmin, xmax = df[x_col].min(), df[x_col].max()
    # ymin, ymax = df[y_col].min(), df[y_col].max()

    xlim = [0-.1, 1.1]
    ylim = [0, 2.5]

    lmap = {'r':'R','theta':'Theta'}
    smap = {'Control':'circle','PD':'diamond-open-dot'}

    fig = px.scatter(df, x=x_col, y=y_col, color=gtype_col, color_discrete_map=cmap, width=650, height=497, labels=lmap, symbol='phenotype', symbol_map=smap)

    fig.update_xaxes(range=xlim, nticks=10, zeroline=False)
    fig.update_yaxes(range=ylim, nticks=10, zeroline=False)
    
    fig.update_layout(margin=dict(r=76, t=63, b=75))

    # fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=1))

    fig.update_layout(legend_title_text='Genotype')

    out_dict = {
        'fig': fig,
        'xlim': xlim,
        'ylim': ylim
    }
    
    fig.update_layout(title_text=f'<b>{title}<b>')
    
    return out_dict

def snp_callback():
    st.session_state['old_snp_choice'] = st.session_state['snp_choice']
    st.session_state['snp_choice'] = st.session_state['new_snp_choice']


snp_metrics_path = f'data/hackathon_snp_metrics_deID.txt'
pathogenic_snps_path = f'data/PATHOGENIC_SNPS_TO_CLUSTER.txt'

snp_metrics = pd.read_csv(snp_metrics_path, sep='\t')
# print(snp_metrics.head())
# print(snp_metrics.columns)
snp_metrics['merge_id'] = 'chr' + snp_metrics['chromosome'].astype(str) + ':' + snp_metrics['position'].astype(str)
# print(snp_metrics.head())
# print(snp_metrics.shape)

pathogenic_snps = pd.read_csv(pathogenic_snps_path, sep='\t')
pathogenic_snps[['chr','pos','alt','ref']] = pathogenic_snps['SNP'].str.split(':', expand=True)
pathogenic_snps['merge_id'] =  pathogenic_snps['chr'].astype(str) + ':' + pathogenic_snps['pos']
# print(pathogenic_snps.head())
# print(pathogenic_snps.shape)

merge1 = snp_metrics.merge(pathogenic_snps, how='left', on=['merge_id'])
merge1 = merge1.drop_duplicates()
# print(merge1.head())
# print(merge1.shape)
# print(merge1.columns)

st.title('Cluster Plot Browser')

metric1,metric2 = st.columns([1,1])

num_snps = len(merge1['snpID'].unique())
num_sample_metrics = len(merge1['Sample_ID'].unique())

merge1 = merge1.drop(columns=['GenTrain_Score','chromosome','position'])

# get SNP options
snp_options = ['Select SNP!']+[snp for snp in merge1['SNP'].unique()]

# set default SNPs
if 'snp_choice' not in st.session_state:
    st.session_state['snp_choice'] = snp_options[0]
if 'old_snp_choice' not in st.session_state:
    st.session_state['old_snp_choice'] = ""

if st.session_state['snp_choice'] in snp_options:
    index = snp_options.index(st.session_state['snp_choice'])

if st.session_state['snp_choice'] not in snp_options:
    if ((st.session_state['snp_choice'] != 'Select SNP!') and (int(st.session_state['snp_choice'].split('(')[1].split(':')[0]) == st.session_state['old_chr_choice'])):
        index = 0

st.markdown('### Select SNP for Cluster Plot')

st.session_state['snp_choice'] = st.selectbox(label='SNP', label_visibility='collapsed', options=snp_options, index=index, key='new_snp_choice', on_change=snp_callback)

if st.session_state['snp_choice'] != 'Select SNP!':
    snp_df = merge1[merge1['SNP'] == st.session_state['snp_choice']]
    snp_df = snp_df.reset_index(drop=True)

    fig = plot_clusters(snp_df, x_col='Theta', y_col='R', gtype_col='GT', title=st.session_state['snp_choice'])['fig']
    st.plotly_chart(fig, use_container_width=True)
