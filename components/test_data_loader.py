import pandas as pd
import streamlit as st

def test_excel_files():
    """Test loading and examining the Excel files"""
    
    files = {
        'escolas': 'escolas_rio.xlsx',
        'ideb_iniciais': 'ideb_iniciais.xlsx', 
        'ideb_finais': 'ideb_finais.xlsx'
    }
    
    for name, filename in files.items():
        try:
            print(f"\n=== Testing {name} ({filename}) ===")
            df = pd.read_excel(filename)
            print(f"Shape: {df.shape}")
            print(f"Columns: {list(df.columns)}")
            print(f"First few rows:")
            print(df.head(2))
            
        except Exception as e:
            print(f"Error loading {filename}: {e}")

if __name__ == "__main__":
    test_excel_files()