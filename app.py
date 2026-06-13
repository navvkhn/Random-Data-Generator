import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io

# Page configuration
st.set_page_config(page_title="Advanced Data Generator", layout="wide")
st.title('Advanced Random Data Generator')

# Predefined themes for Text generation
THEMES = {
    "Generic": ['Alpha', 'Beta', 'Gamma', 'Delta', 'Valid', 'Null_Check', 'Test_Row'],
    "Racing": ['F1', 'Nascar', 'Pitstop', 'Lap_Time', 'Driver', 'Circuit', 'Chassis', 'Grid'],
    "Bike Sales": ['Mountain', 'Road', 'Hybrid', 'BMX', 'Electric', 'Gear', 'Spoke', 'Frame'],
    "Hospital": ['Patient', 'Doctor', 'Ward', 'Emergency', 'ICU', 'Discharged', 'Admitted', 'Triage']
}

def sidebar_config():
    st.sidebar.header('1. Core Settings')
    
    # Theme selection
    selected_theme = st.sidebar.selectbox("Select Data Theme (for Text columns)", list(THEMES.keys()))
    
    # Shape inputs
    num_rows = st.sidebar.number_input("Number of Rows", min_value=1, max_value=100000, value=1000)
    num_cols = st.sidebar.number_input("Number of Columns", min_value=1, max_value=50, value=5)

    st.sidebar.header('2. Global Data Ranges')
    # Use expanders to keep the sidebar tidy
    with st.sidebar.expander("Integer & Float Ranges"):
        int_min = st.number_input("Integer Minimum", value=-1000)
        int_max = st.number_input("Integer Maximum", value=1000)
        float_min = st.number_input("Float Minimum", value=0.0)
        float_max = st.number_input("Float Maximum", value=1000.0)

    with st.sidebar.expander("Date Ranges & Custom Text"):
        start_date = st.date_input("Start Date", datetime.now() - timedelta(days=365))
        end_date = st.date_input("End Date", datetime.now())
        custom_words = st.text_input("Custom Text Words (Comma separated)", placeholder="Apple, Banana, Cherry")

    # Safety checks for ranges
    if int_min >= int_max: int_max = int_min + 1
    if float_min >= float_max: float_max = float_min + 1.0
    if start_date >= end_date: end_date = start_date + timedelta(days=1)

    # Determine final word list
    if custom_words.strip():
        word_list = [w.strip() for w in custom_words.split(',')]
    else:
        word_list = THEMES[selected_theme]

    st.sidebar.header('3. Column Configuration')
    col_configs = []
    
    with st.sidebar.expander("Rename & Type Columns", expanded=True):
        for i in range(num_cols):
            col1, col2 = st.columns([3, 2])
            # Ensure unique keys for dynamically generated Streamlit widgets
            c_name = col1.text_input("Name", value=f"{selected_theme}_Col_{i+1}", key=f"name_{i}", label_visibility="collapsed")
            c_type = col2.selectbox("Type", ["Integers", "Floats", "Dates", "Text"], key=f"type_{i}", label_visibility="collapsed")
            col_configs.append((c_name, c_type)) # Stored as tuple for caching

    # Package settings to pass to generator
    ranges = {
        "int_range": (int_min, int_max),
        "float_range": (float_min, float_max),
        "date_range": (start_date, end_date),
        "words": tuple(word_list) # Convert to tuple for hashing
    }
    
    return num_rows, tuple(col_configs), ranges

# Cache data so it doesn't regenerate when user clicks a download button
@st.cache_data
def generate_dataset(rows, col_configs, ranges):
    data_dict = {}
    
    # Unpack ranges
    int_min, int_max = ranges["int_range"]
    float_min, float_max = ranges["float_range"]
    start_date, end_date = ranges["date_range"]
    words = ranges["words"]
    
    for c_name, c_type in col_configs:
        # Handle duplicate column names gracefully by appending a random string
        final_col_name = c_name
        if final_col_name in data_dict:
            final_col_name = f"{c_name}_{np.random.randint(100, 999)}"
            
        if c_type == "Integers":
            data_dict[final_col_name] = np.random.randint(int_min, int_max + 1, size=rows)
            
        elif c_type == "Floats":
            data_dict[final_col_name] = np.random.uniform(float_min, float_max, size=rows).round(4)
            
        elif c_type == "Dates":
            days_diff = (end_date - start_date).days
            random_days = np.random.randint(0, days_diff, size=rows)
            data_dict[final_col_name] = [start_date + timedelta(days=int(d)) for d in random_days]
            
        elif c_type == "Text":
            data_dict[final_col_name] = np.random.choice(words, size=rows)
            
    return pd.DataFrame(data_dict)

def main():
    # 1. Fetch UI configurations
    rows, col_configs, ranges = sidebar_config()

    if st.sidebar.button("Generate New Dataset", type="primary"):
        st.cache_data.clear()
        
    # 2. Generate Data
    df = generate_dataset(rows, col_configs, ranges)
    
    # 3. Display Data
    st.subheader(f'Dataset Preview ({rows} rows, {len(col_configs)} columns)')
    st.dataframe(df.head(100)) # Preview first 100 to keep UI snappy
    
    # 4. Export Options
    st.subheader('Export Options')
    col1, col2 = st.columns(2)
    
    # CSV Export
    csv = df.to_csv(index=False).encode('utf-8')
    col1.download_button(
        label="Download as CSV",
        data=csv,
        file_name="custom_dataset.csv",
        mime="text/csv"
    )
    
    # Excel Export
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Data')
        
    col2.download_button(
        label="Download as Excel",
        data=buffer,
        file_name="custom_dataset.xlsx",
        mime="application/vnd.ms-excel"
    )

if __name__ == "__main__":
    main()
