import pandas as pd
import numpy as np

def profile_dataframe(df: pd.DataFrame) -> dict:
    profile = {
        "rows": len(df),
        "columns": []
    }
    
    for col in df.columns:
        col_data = df[col]
        dtype = str(col_data.dtype)
        
        col_info = {
            "name": col,
            "type": dtype,
            "missing": int(col_data.isna().sum()),
            "unique": int(col_data.nunique())
        }
        
        # Add stats for numeric columns
        if pd.api.types.is_numeric_dtype(col_data):
            col_info["min"] = float(col_data.min()) if not pd.isna(col_data.min()) else None
            col_info["max"] = float(col_data.max()) if not pd.isna(col_data.max()) else None
            col_info["mean"] = float(col_data.mean()) if not pd.isna(col_data.mean()) else None
            
        profile["columns"].append(col_info)
        
    return profile
