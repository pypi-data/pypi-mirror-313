"""
Data processing utilities.
"""
from typing import Dict, List, Any
import pandas as pd

def process_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Process a DataFrame to prepare it for Argilla.
    
    Args:
        df: Input DataFrame to process
        
    Returns:
        Processed DataFrame
    """
    # Add your processing logic here
    processed_df = df.copy()
    
    # Clean text fields
    text_columns = ['prompt', 'response', 'context', 'keywords']
    for col in text_columns:
        if col in processed_df.columns:
            processed_df[col] = processed_df[col].fillna('')
            processed_df[col] = processed_df[col].astype(str)
            processed_df[col] = processed_df[col].str.strip()
    
    # Convert dates
    if 'conversation_date' in processed_df.columns:
        processed_df['conversation_date'] = pd.to_datetime(
            processed_df['conversation_date']
        ).dt.strftime('%Y-%m-%d')
    
    return processed_df

def clean_text_field(text: str) -> str:
    """
    Clean a text field by removing extra whitespace and normalizing.
    
    Args:
        text: Input text to clean
        
    Returns:
        Cleaned text
    """
    if pd.isna(text):
        return ""
    return str(text).strip()
