# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 14:46:20 2024

@author: Joseph Rosen

Package file containing Visualization functions for mafViper


"""

# Importing dependencies
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from .mafProcessing import classify_variants, get_titv


  
def get_maf_summary(maf_df, output_pdf: str = None, add_stat: str = None, show_barcodes: bool = False, top_genes: int = 10, raw_count: bool = True, nonsyn_titv: bool = False, use_nonsyn: bool = True):
    if output_pdf is None:
        output_pdf = "MAF_Summary_Dashboard.pdf"
        
    # Summarize Data & filter maf df for non-syn mutations if needed
    if use_nonsyn:
        nonsyn_df = classify_variants(maf_df, discard_synonymous= True)
        maf_data_df = nonsyn_df
    else:
        maf_data_df = maf_df
    
    # Variant classification calculation
    variant_classification = maf_data_df['Variant_Classification'].value_counts().reset_index()
    variant_classification.columns = ['Variant_Classification', 'Count']
    
    gene_summary = maf_data_df.groupby('Hugo_Symbol').size().reset_index(name='Mutation_Count').nlargest(top_genes, 'Mutation_Count')
    variant_type = maf_data_df['Variant_Type'].value_counts().reset_index()
    variant_type.columns = ['Variant_Type', 'Count']
    
    # Setting Data Source based on non-synonymous mutation preference
    # default for titv is synonymous counts- maftools precedent
    if nonsyn_titv: 
        snv_summary_df = get_titv(nonsyn_df)
    else:
        snv_summary_df = get_titv(maf_df)
    
    # Normalize Ti/Tv data if proportions are requested
    if not raw_count:
        SNV_x_col = 'Proportion'
        SNV_x_label = 'Proportion'
    else:
        SNV_x_col = 'Raw_Count'
        SNV_x_label = 'Raw Count'
    
    # Dashboard Plot
    with PdfPages(output_pdf) as pdf:
        fig, axes = plt.subplots(3, 2, figsize=(15, 20)) #3 row 2 col

         # Plot 1: Stacked Bar Chart for Variants Per Sample
        sample_variant_type = maf_data_df.groupby(['Tumor_Sample_Barcode', 'Variant_Type']).size().reset_index(name='Count')
        sample_variant_type_pivot = sample_variant_type.pivot(index='Tumor_Sample_Barcode', columns='Variant_Type', values='Count').fillna(0)

        sample_variant_type_pivot.plot(kind='bar', stacked=True, ax=axes[0, 0], colormap='viridis', edgecolor='none')
        axes[0, 0].set_title('Variants Per Sample', fontsize=12)
        axes[0, 0].set_xlabel('Sample', fontsize=10)
        axes[0, 0].set_ylabel('Mutation Count', fontsize=10)

        # Add mean or median line if specified
        if add_stat:
            if add_stat == 'mean':
                stat_value = sample_variant_type_pivot.sum(axis=1).mean()
            elif add_stat == 'median':
                stat_value = sample_variant_type_pivot.sum(axis=1).median()
            axes[0, 0].axhline(stat_value, color='red', linestyle='--', label=f'{add_stat.capitalize()}: {stat_value:.2f}')
            axes[0, 0].legend()

        # Plot 2: Variant Classification Summary
        sns.barplot(x='Variant_Classification', y='Count', data=variant_classification, ax=axes[0, 1], hue='Variant_Classification', palette='viridis', legend=False)
        axes[0, 1].set_title('Variant Classification Summary')
        axes[0, 1].set_xlabel('Variant Classification')
        axes[0, 1].set_ylabel('Count')
        axes[0, 1].tick_params(axis='x', rotation=45)

        # Plot 3: Top Mutated Genes
        sns.barplot(y='Hugo_Symbol', x='Mutation_Count', data=gene_summary, ax=axes[1, 0], hue='Hugo_Symbol', palette='viridis', legend=False)
        axes[1, 0].set_title(f'Top {top_genes} Mutated Genes')
        axes[1, 0].set_xlabel('Mutation Count')
        axes[1, 0].set_ylabel('Gene')
        axes[1, 0].set_xlim(0, 4)

        # Plot 4: Boxplot for Variant Classification
        sns.boxplot(x='Variant_Classification', y='t_alt_count', data=maf_data_df, ax=axes[1, 1], hue='Variant_Classification', palette='viridis', legend=False)
        axes[1, 1].set_title('Boxplot of Variant Classification Counts')
        axes[1, 1].set_xlabel('Variant Classification')
        axes[1, 1].set_ylabel('Alternate Allele Counts')
        axes[1, 1].tick_params(axis='x', rotation=45)
        
        # Plot 5: SNV Class Summary (Ti/Tv Data)
        if not raw_count:
            sns.barplot(data=snv_summary_df, x=SNV_x_col, y='SNV_Class', ax=axes[2, 0], hue= 'SNV_Class', palette='viridis', orient='h')
            axes[2, 0].set_xlim(0, 100)  # Set x-axis limit to percentage
            for i, value in enumerate(snv_summary_df['Proportion']):
                axes[2, 0].text(value + 1, i, f"{snv_summary_df['Raw_Count'].iloc[i]}", va='center', fontsize=9)
        else:
            sns.barplot(data=snv_summary_df, x=SNV_x_col, y='SNV_Class', ax=axes[2, 0], palette='viridis', orient='h')
        
        axes[2, 0].set_title('SNV Class Summary')
        axes[2, 0].set_xlabel(SNV_x_label, fontsize=10)
        axes[2, 0].set_ylabel('SNV Class')

        # Plot 6: Variant Type Summary (e.g., SNP, INS, DEL)
        sns.barplot(x='Variant_Type', y='Count', data=variant_type, ax=axes[2, 1], hue='Variant_Type', palette='viridis',  legend=False)
        axes[2, 1].set_title('Variant Type Summary')
        axes[2, 1].set_xlabel('Variant Type')
        axes[2, 1].set_ylabel('Count')
      
        # Tight layout and save PDF
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.show()
        pdf.savefig(fig)
        plt.close(fig)

    print(f"Summary dashboard saved to: {output_pdf}")