# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 14:42:05 2024

@author: Joseph Rosen

Maf processing functions file:

Contains functions for the processing of maf dataframes    

"""

import pandas as pd



def classify_variants(maf, discard_synonymous= True):
    """
    Separates variants into synonymous and non-synonymous categories.
    """
    non_synonymous = [
        "Frame_Shift_Del", "Frame_Shift_Ins", "Splice_Site", "Translation_Start_Site",
        "Nonsense_Mutation", "Nonstop_Mutation", "In_Frame_Del",
        "In_Frame_Ins", "Missense_Mutation"
    ]
    if discard_synonymous:
        maf = maf[maf['Variant_Classification'].isin(non_synonymous)]
    return maf

def merge_mafs(maf_list, discard_synonymous= False):
    """
    Merges multiple MAF DataFrames into one.

    Parameters:
        maf_list (list): List of MAF DataFrames to merge.

    Returns:
        pd.DataFrame: Merged MAF DataFrame.
    """
    merged_maf = pd.concat(maf_list, axis=0, ignore_index=True)
    merged_maf = merged_maf.drop_duplicates(subset=['Hugo_Symbol', 'Chromosome', 'Start_Position', 'End_Position', 'Tumor_Sample_Barcode'])
    
    if discard_synonymous == True:
        merged_maf = classify_variants(merged_maf, discard_synonymous = True)
        return merged_maf
    
    return merged_maf

def get_titv(maf_df):
    """
    Classify SNVs into Ti/Tv and generate summary for plotting.

    Parameters:
        maf_df (pd.DataFrame): MAF DataFrame containing at least the columns:
                               ['Reference_Allele', 'Tumor_Seq_Allele2', 'Variant_Type'].

    Returns:
        pd.DataFrame: Summary DataFrame with SNV class counts and Ti/Tv classification.
    """
    # Create a copy to avoid SettingWithCopyWarning
    maf_snv_df = maf_df[maf_df['Variant_Type'] == 'SNP'].copy()
    
    # Use .loc for setting new columns
    maf_snv_df.loc[:, 'SNV_Class'] = maf_snv_df['Reference_Allele'] + '>' + maf_snv_df['Tumor_Seq_Allele2']
    
    conv = {
        'A>G': 'T>C', 'T>C': 'T>C',
        'C>T': 'C>T', 'G>A': 'C>T',
        'A>T': 'T>A', 'T>A': 'T>A',
        'A>C': 'T>G', 'T>G': 'T>G',
        'C>A': 'C>A', 'G>T': 'C>A',
        'C>G': 'C>G', 'G>C': 'C>G'
    }
    conv_class = {
        'T>C': 'Ti', 'C>T': 'Ti',
        'T>A': 'Tv', 'T>G': 'Tv',
        'C>A': 'Tv', 'C>G': 'Tv'
    }
    
    # Use .loc for mapping
    maf_snv_df.loc[:, 'SNV_Class'] = maf_snv_df['SNV_Class'].map(conv)
    maf_snv_df.loc[:, 'TiTv'] = maf_snv_df['SNV_Class'].map(conv_class)
    
    maf_snv_df = maf_snv_df.dropna(subset=['SNV_Class', 'TiTv'])

    snv_summary_df = (
        maf_snv_df.groupby('SNV_Class')
        .size()
        .reset_index(name='Raw_Count')
    )
    total_variants = snv_summary_df['Raw_Count'].sum()
    snv_summary_df['Proportion'] = (snv_summary_df['Raw_Count'] / total_variants) * 100
    return snv_summary_df



