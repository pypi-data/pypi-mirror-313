"""
Data loading utilities.
"""
from typing import Dict, Any
import pandas as pd

def load_csv_files(file_paths: Dict[str, str]) -> Dict[str, pd.DataFrame]:
    """
    Load CSV files into pandas DataFrames.
    
    Args:
        file_paths: Dictionary mapping DataFrame names to file paths
        
    Returns:
        Dictionary mapping names to loaded DataFrames
    """
    dataframes = {}
    for name, path in file_paths.items():
        dataframes[name] = pd.read_csv(path)
    return dataframes
