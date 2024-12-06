# mafViper Documentation

A python package for reading, analyzing and visualizing mutation annotation files

## Features

- Load and validate MAF files as pandas DataFrames.

- MAF processsing and classification tools (i.e synonymous vs. non-synonymous)

- Merge multiple MAF files into a single DF. 

- Generate mutation summary plots, and Ti/Tv analyses. 


## Current Functions

* **read_maf**: 
	- Loads a maf file into the env as a pandas df and validates columns
	- allows for somatic vs. non-somatic selection with useAll parameter

* **classify_variants**:
	- Seperates variants into synonymous and non-synonmous categories
	- discard_synonymous (default True) allows you to drop synonymous mutations from dataframe
* **merge_mafs**:
	- merges a list of maf files into one maf
	- discard_synonymous parameter allows you to drop synonymous mutations after merge
* **get_titv**:
	- Classifies SNVs into Ti/Tv and returns a summary df for plotting and analyses
	- Summary df contains SNV class, Raw counts by class, and fractional proportions of each class 

* **get_maf_summary**:
	- creates a set of maf summary analysis plots and pdf per user input 
	- Top Mutated Genes plot (default 10)
	- Stacked Bar chart for Variants Per Sample (add stat line- default median)
	- Variant Classifaction Summary Plot
	- Boxplot of variant classes 
	- SNV Class summary  plot(Ti/Tv data visualization)
	- Variant Type summary plot (SNP, INS, DEL, etc)

## Installation

'''bash

pip install mafViper

 
