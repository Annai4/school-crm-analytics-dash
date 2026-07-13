import pandas as pd
import re

def standardize_df(df):
    if df is None:
        return None

    df = df.copy()
    for col in df.columns:
        
        if df[col].dtype == 'object':
            df[col] = (
                df[col]
                .astype(str)
                .str.strip()         
                .str.lower()         
                .str.replace(r"[ \-]", "_", regex=True) 
                .replace('nan', 'unknown')
            )
    return df


def apply_standardization(obj):
   
    tables = ['d1', 'd2', 'd3', 'd4']

    for t in tables:
        current_df = getattr(obj, t, None)

        if current_df is not None:
            cleaned_df = standardize_df(current_df)
            setattr(obj, t, cleaned_df)

            if t in obj.clean:
                obj.clean[t] = cleaned_df

    return obj