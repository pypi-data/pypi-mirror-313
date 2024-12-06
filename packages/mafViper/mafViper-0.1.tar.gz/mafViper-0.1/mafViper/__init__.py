# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 14:19:57 2024

@author: Joseph Rosen

initialization file
"""

# Import main functions from submodules
from .mafLoadr import read_maf
from .mafProcessing import classify_variants, merge_mafs, get_titv
from .mafVisualization import get_maf_summary

# Define what should be accessible when the package is imported
__all__ = [
    'read_maf',
    'classify_variants',
    'merge_mafs',
    'get_titv',
    'get_maf_summary'
]

# Optional metadata
__version__ = "0.1"
__author__ = "Joseph Rosen"

