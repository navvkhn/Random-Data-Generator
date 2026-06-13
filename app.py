import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io

# Page configuration
st.set_page_config(page_title="Data Generator Suite", layout="wide")
st.title('Random Data Generator and Exporter')

def sidebar_config():
    st.sidebar.header('Configuration')
    
    # Simplified shape inputs
    num_rows = st.sidebar.number_input("Number of Rows", min_value=1, max_value=50000, value=1000)
    num_cols = st.sidebar.number_input("Number of Columns", min_value=1, max_value=100, value=5)
    
    # Data type selection
    data_types = st.sidebar.multiselect(
        "Select Data Types to Include",
        options=["Integers", "Floats", "Dates", "Text"],  # Changed 'choices' to 'options'
        default=["Integers", "Floats", "Text"]
    )
    
    return num_rows, num_cols, data_types
# Cache the data generation so it doesn't regenerate on download button clicks
@st.cache_data
def generate_dataset(rows, cols, types):
    if not types:
        return pd.DataFrame()
        
    data_dict = {}
    
    for i in range(cols):
        # Cycle evenly through the selected data types for the columns
        col_type = types[i % len(types)] 
        col_name = f"Col_{chr(65 + i)}_{col_type}"
        
        if col_type == "Integers":
            data_dict[col_name] = np.random.randint(-10000, 10000, size=rows)
            
        elif col_type == "Floats":
            data_dict[col_name] = np.random.uniform(0.1, 1000.0, size=rows).round(4)
            
        elif col_type == "Dates":
            start_date = datetime.now() - timedelta(days=365)
            # Add random days to the start date
            random_days = np.random.randint(0, 365, size=rows)
            data_dict[col_name] = [start_date + timedelta(days=int(d)) for d in random_days]
            
        elif col_type == "Text":
            sample_words = ['Alpha', 'Beta', 'Gamma', 'Test_Row', 'Data_Point', 'Valid', 'Null_Check']
            data_dict[col_name] = np.random.choice(sample_words, size=rows)
            
    return pd.DataFrame(data_dict)

def main():
    # 1. Sidebar Setup
    rows, cols, data_types = sidebar_config()
    
    if not data_types:
        st.warning("Please select at least one data type from the sidebar to generate data.")
        return

    # Button to force regeneration by clearing the cache
    if st.sidebar.button("Generate New Dataset"):
        st.cache_data.clear()
        
    # 2. Generate Data
    df = generate_dataset(rows, cols, data_types)
    
    # 3. Display Data
    st.subheader(f'Dataset Preview ({rows} rows, {cols} columns)')
    st.dataframe(df.head(100)) # Preview first 100 rows to save memory
    
    # 4. Export Options
    st.subheader('Export Options')
    col1, col2 = st.columns(2)
    
    # CSV Export
    csv = df.to_csv(index=False).encode('utf-8')
    col1.download_button(
        label="Download as CSV",
        data=csv,
        file_name="test_dataset.csv",
        mime="text/csv"
    )
    
    # Excel Export (requires 'xlsxwriter' or 'openpyxl' installed)
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        
    col2.download_button(
        label="Download as Excel",
        data=buffer,
        file_name="test_dataset.xlsx",
        mime="application/vnd.ms-excel"
    )

if __name__ == "__main__":
    main()
