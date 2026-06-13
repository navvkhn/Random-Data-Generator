import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io
import random

# Page configuration
st.set_page_config(page_title="Advanced Data Generator", layout="wide")
st.title('Advanced Random Data Generator & Synthesizer')

# Predefined themes for Text generation
THEMES = {
    "Generic": ['Alpha', 'Beta', 'Gamma', 'Delta', 'Valid', 'Null_Check', 'Test_Row'],
    "Racing": ['F1', 'Nascar', 'Pitstop', 'Lap_Time', 'Driver', 'Circuit', 'Chassis', 'Grid'],
    "Bike Sales": ['Mountain', 'Road', 'Hybrid', 'BMX', 'Electric', 'Gear', 'Spoke', 'Frame'],
    "Hospital": ['Patient', 'Doctor', 'Ward', 'Emergency', 'ICU', 'Discharged', 'Admitted', 'Triage']
}

# Real-world lookup repositories for semantic data generation
FIRST_NAMES = ['John', 'Jane', 'Alex', 'Emily', 'Michael', 'Sarah', 'David', 'Jessica', 'James', 'Maria', 'Robert', 'Lisa', 'William', 'Karen', 'Joseph', 'Donna']
LAST_NAMES = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas']
DOMAINS = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'protonmail.com', 'icloud.com']
COMPANIES = ['ApexCorp', 'VertexIndustries', 'NovaLogistics', 'QuantumTech', 'BlueSkyHolding', 'SummitMedia', 'IronCladSecurity', 'CoreSolutions']
CITIES = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose']
STATES = ['NY', 'CA', 'IL', 'TX', 'AZ', 'PA', 'TX', 'CA', 'TX', 'CA']

def sidebar_config():
    st.sidebar.header('1. Core Settings')
    
    # Theme selection
    selected_theme = st.sidebar.selectbox("Select Keyword Theme (for Generic Text columns)", list(THEMES.keys()))
    
    # Shape inputs
    num_rows = st.sidebar.number_input("Number of Rows", min_value=1, max_value=100000, value=1000)
    num_cols = st.sidebar.number_input("Number of Columns", min_value=1, max_value=50, value=5)

    st.sidebar.header('2. Global Data Ranges')
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

    # Determine final word list for generic text columns
    if custom_words.strip():
        word_list = [w.strip() for w in custom_words.split(',')]
    else:
        word_list = THEMES[selected_theme]

    st.sidebar.header('3. Column Configuration')
    col_configs = []
    
    # Expanded list of structural and semantic data types
    available_types = [
        "Integers", "Floats", "Dates", "Text (Theme-Based)", 
        "Full Name", "Email Address", "Company Name", "Phone Number", "City & State"
    ]
    
    with st.sidebar.expander("Rename & Classify Columns", expanded=True):
        for i in range(num_cols):
            col1, col2 = st.columns([3, 2])
            
            # Smart default naming logic based on selection index
            default_name = f"Field_{i+1}"
            if i == 0: default_name = "Customer_ID" if "Hospital" not in selected_theme else "Patient_ID"
            elif i == 1: default_name = "Full_Name"
            elif i == 2: default_name = "Email"
            
            c_name = col1.text_input("Name", value=default_name, key=f"name_{i}", label_visibility="collapsed")
            
            # Distribute default types cleanly across the list
            default_type_idx = min(i, len(available_types)-1) if i < 4 else random.randint(0, len(available_types)-1)
            c_type = col2.selectbox("Type", available_types, index=default_type_idx, key=f"type_{i}", label_visibility="collapsed")
            
            col_configs.append((c_name, c_type))

    # Package settings to pass to generator
    ranges = {
        "int_range": (int_min, int_max),
        "float_range": (float_min, float_max),
        "date_range": (start_date, end_date),
        "words": tuple(word_list)
    }
    
    return num_rows, tuple(col_configs), ranges

@st.cache_data
def generate_dataset(rows, col_configs, ranges):
    data_dict = {}
    
    # Unpack basic configurations
    int_min, int_max = ranges["int_range"]
    float_min, float_max = ranges["float_range"]
    start_date, end_date = ranges["date_range"]
    words = ranges["words"]
    
    for c_name, c_type in col_configs:
        # Handle duplicate column names gracefully
        final_col_name = c_name
        if final_col_name in data_dict:
            final_col_name = f"{c_name}_{np.random.randint(100, 999)}"
            
        # 1. Base Structural Types
        if c_type == "Integers":
            data_dict[final_col_name] = np.random.randint(int_min, int_max + 1, size=rows)
            
        elif c_type == "Floats":
            data_dict[final_col_name] = np.random.uniform(float_min, float_max, size=rows).round(4)
            
        elif c_type == "Dates":
            days_diff = (end_date - start_date).days
            random_days = np.random.randint(0, max(1, days_diff), size=rows)
            data_dict[final_col_name] = [start_date + timedelta(days=int(d)) for d in random_days]
            
        elif c_type == "Text (Theme-Based)":
            data_dict[final_col_name] = np.random.choice(words, size=rows)
            
        # 2. Complex Real-World Semantic Types
        elif c_type == "Full Name":
            fn = np.random.choice(FIRST_NAMES, size=rows)
            ln = np.random.choice(LAST_NAMES, size=rows)
            data_dict[final_col_name] = [f"{f} {l}" for f, l in zip(fn, ln)]
            
        elif c_type == "Email Address":
            fn = np.random.choice(FIRST_NAMES, size=rows)
            ln = np.random.choice(LAST_NAMES, size=rows)
            dom = np.random.choice(DOMAINS, size=rows)
            data_dict[final_col_name] = [f"{f.lower()}.{l.lower()}@{d}" for f, l, d in zip(fn, ln, dom)]
            
        elif c_type == "Company Name":
            data_dict[final_col_name] = np.random.choice(COMPANIES, size=rows)
            
        elif c_type == "Phone Number":
            area_codes = np.random.randint(200, 999, size=rows)
            prefixes = np.random.randint(100, 999, size=rows)
            line_numbers = np.random.randint(1000, 9999, size=rows)
            data_dict[final_col_name] = [f"+1 ({a}) {p}-{l}" for a, p, l in zip(area_codes, prefixes, line_numbers)]
            
        elif c_type == "City & State":
            indices = np.random.randint(0, len(CITIES), size=rows)
            data_dict[final_col_name] = [f"{CITIES[idx]}, {STATES[idx]}" for idx in indices]
            
    return pd.DataFrame(data_dict)

def main():
    rows, col_configs, ranges = sidebar_config()

    if st.sidebar.button("Generate New Dataset", type="primary"):
        st.cache_data.clear()
        
    df = generate_dataset(rows, col_configs, ranges)
    
    # Render Preview Window
    st.subheader(f'Dataset Preview ({rows} rows, {len(col_configs)} columns)')
    st.dataframe(df.head(100))
    
    # Export options block
    st.subheader('Export Options')
    col1, col2 = st.columns(2)
    
    # CSV Data Pipeline
    csv = df.to_csv(index=False).encode('utf-8')
    col1.download_button(
        label="Download as CSV",
        data=csv,
        file_name="synthetic_analytics_dataset.csv",
        mime="text/csv"
    )
    
    # Excel Object Generation
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Synthetic_Data')
        
    col2.download_button(
        label="Download as Excel",
        data=buffer,
        file_name="synthetic_analytics_dataset.xlsx",
        mime="application/vnd.ms-excel"
    )

if __name__ == "__main__":
    main()
