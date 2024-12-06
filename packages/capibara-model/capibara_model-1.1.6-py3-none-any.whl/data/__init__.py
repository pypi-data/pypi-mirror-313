"""
Data Package for CapibaraModel

This package provides modules and utilities for data loading and preprocessing.

Modules:
    - data_loader: Handles data loading for the CapibaraModel.
    - dataset: Manages datasets for training and evaluation.
    
Exports:
    - CapibaraDataLoader: Class for efficient data loading.
    - CapibaraDataset: Class for byte-based dataset handling.
"""

# Import necessary classes
from .dataset import CapibaraDataset
from .data_loader import CapibaraDataLoader

__all__ = [
    "CapibaraDataset",
    "CapibaraDataLoader"
]
