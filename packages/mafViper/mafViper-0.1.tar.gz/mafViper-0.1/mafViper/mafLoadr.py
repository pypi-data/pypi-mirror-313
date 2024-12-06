# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 14:33:21 2024

@author: Joseph Rosen

Maf Reader functions file

Contains Functions for loading a maf into a python environment as a dataframe

"""

import pandas as pd

def read_maf(maf_file, skip_rows_until="Hugo_Symbol", sep="\t", use_all= True):
    """
    Reads a MAF file, skipping lines until the specified header is found.
    
    Parameters:
        maf_file (str): Path to the MAF file.
        skip_rows_until (str): Column name to start reading from.
        sep (str): Delimiter used in the MAF file (default is tab).
        
    Returns:
        pd.DataFrame: Loaded MAF file as a DataFrame.
    """
    with open(maf_file, 'r') as f:
        for i, line in enumerate(f):
            if line.startswith(skip_rows_until):
                skip_rows = i
                break
    maf_df = pd.read_csv(maf_file, sep=sep, skiprows=skip_rows, comment="#")
    

    def validate_maf(maf_df, use_all=use_all):
        """
        Validates and filters the MAF DataFrame.
        
        Parameters:
            maf_df (pd.DataFrame): DataFrame containing MAF data.
            use_all (bool): If False, only keep variants with Mutation_Status = 'Somatic'.
            
        Returns:
            pd.DataFrame: Validated MAF DataFrame.
        """
        required_cols = [
            'Hugo_Symbol', 'Chromosome', 'Start_Position', 'End_Position',
            'Reference_Allele', 'Tumor_Seq_Allele2', 'Variant_Classification', 'Tumor_Sample_Barcode', 'Variant_Type'
        ]
        for col in required_cols:
            if col not in maf_df.columns:
                raise ValueError(f"Missing required column: {col}")
        if not use_all and 'Mutation_Status' in maf_df.columns:
            maf_df = maf_df[maf_df['Mutation_Status'] == 'Somatic']
        return maf_df
    maf_df = validate_maf(maf_df, use_all=use_all)
        
    
    return maf_df
