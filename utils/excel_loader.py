import pandas as pd

EXCEL_FILE = "Smart Dashboard - 19 Punjab.xlsx"

def load_sheet(sheet_name):
    return pd.read_excel(
        EXCEL_FILE,
        sheet_name=sheet_name,
        header=None
    )
    
def clean_column_names(df):

    df.columns = (
        pd.Index(df.columns)
        .astype(str)
        .str.replace("\n", " ", regex=False)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )

    return df