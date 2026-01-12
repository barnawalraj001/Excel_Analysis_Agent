from fastapi import UploadFile, HTTPException
import pandas as pd
import io

async def load_file(file: UploadFile) -> pd.DataFrame:
    content = await file.read()
    filename = file.filename.lower()
    
    try:
        if filename.endswith(".csv"):
            df = pd.read_csv(io.BytesIO(content))
        elif filename.endswith((".xls", ".xlsx")):
            df = pd.read_excel(io.BytesIO(content), engine="openpyxl")
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format. Please upload .csv or .xlsx")
        
        return df
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading file: {str(e)}")
