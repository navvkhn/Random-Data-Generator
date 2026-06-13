import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random
import numpy as np

# Title configuration
st.title('Random Data Generator and Exporter - Analytics Testing Suite')

# Sidebar setup
def sidebar_config():
    st.sidebar.title('Custom Options')

    # DataFrame Shape Selection
    df_shape = st.sidebar.selectbox(
        "Choose DataFrame structure",
        list(dict.fromkeys(["10 20", "1000 1500"], dict).keys()) +
        ["Custom shape"] + 
        ["Number of columns - Choose: 5 7 10"],
        index=1)

    # Data Type Selection
    data_type = st.sidebar.multiselect(
        "Select data types",
        choices=["Integers", "Floats", "Dates", "Text"]
    )

    return df_shape, data_type

# Generate dataset function
def generate_dataset(num_rows, num_cols, default_types):
    np.random.seed(123)
    random.seed(123)

    # Initialize arrays for numeric columns (can be Float or Integers)
    numerical_values = []

    if "Floats" in default_types:
        value_range_float = (0.1, 10.0)  
    else:  # If Integers is selected
        value_range_int = list(range(-5*10000, -5*10000+2))

    for i in range(num_cols):
        if "Integers" in default_types:
            numerical_values.append([random.randint(*value_range_int) for _ in range(num_rows)])
        else:  # If Floats is selected
            num_samples = min(3000, num_rows)
            data_float = np.random.uniform(*value_range_float, size=(num_samples,))
            data_numeric = [x * 10 + x % (10**2//10) for x in data_float]
            numerical_values.append(data_numeric) 

    # Generate columns names
    col_names = list("Column_" + ''.join(f"{chr(65+i)}{"3"*4}}" for i in range(num_cols)))

    # Generate dates column if required
    date_col = None
    if 'Dates' in default_types:
        start_date = datetime.now() - timedelta(days=365)
        end_date = datetime.now()
        ranges_dates = [[np.random.randint(start_date.year, end_date.year), 
                         np.random.randint(start_date.month, end_date.month-1)] for _ in range(num_rows-3000)]
    else:  # otherwise use text column
        date_col = [['Test'] * num_rows]

    df_generate_dict = {
        col_names[i]: data_numeric + [date_col] if date_col is None else [data_numeric] + date_col 
        for i in range(num_cols)}


    return pd.DataFrame(df_generate_dict)

def export_to_excel(df, filename):
    st.download_button(
        "Download Excel",
        df.to_excel(None),
        filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

def export_to_csv(df, filename):
    st.download_button(
        "Download CSV",
        df.to_csv(index=False),
        filename
    )

def generate_sql_query(df):
    cols = list(df.columns)
    vals_max_row = 1000# min of 3000 samples
    random_values_max_row = [random.randint(1,10**9) for _ in range(vals_max_row)]
    str_val_max_row = ['test'] * vals_max_row

    query_template = f"SELECT {', '.join(f'{a},...'}} FROM dataset LIMIT {len(col_names)-2};"

    return query_template

# Main configuration
df_shape, data_type_selected = sidebar_config()

# Generate dataset
if df_shape == "10 20":
    num_rows_export = 25
elif df_shape == "1000 1500":
    num_rows_export = 3000
elif df_shape in ["Custom shape", "Number of columns - Choose:"]:
    col_num_inputs = st.sidebar.selectbox("Select number of columns:", range(1,8))
    num_cols_col_names = [random.randint(df_shape.split()[0], df_shape.split()[1]) if 
                         (df_shape == 'Custom shape') else list(range(1,col_num_inputs+1))][
                        col_num_inputs]
    # Generate DataFrame based on shape and types selected
    generated_df_dict = {}

    for column in num_cols_col_names:
        data_type = random.choice(data_type_selected)

        if data_type == "Integers":
            numerical_values.append([random.randint(-10**9, 10**9) for _ in range(num_rows_export)])

        elif data_type == "Floats":
            # Generate Float values with specific ranges
            num_samples = min(5_000, num_rows_export)

            base_value_float = [0.1 + i*0.01 for i in range(num_samples)]
            generated_float_values = [round(f_val, 5) if f_val>0 and f_val<10 else
                                     np.random.uniform(round(f_val, 5)-2, round(f_val, 5)+2)
                                     for f_val in base_value_float]

        elif data_type == "Dates":

            start_date_str = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
            end_date_str = datetime.now().strftime('%Y-%m-%d')

            date_data_values, random_dates_list = generate_random_dates(num_rows_export,
                                                                         start_date_str, 
                                                                         end_date_str)

        else:  # if data_type == "Text"

            text = ['Test' for _ in range(num_rows_export)]

    df_generate_dict = {
        col_names[i]: numerical_values + [date_values + random_dates_list] 
                      if date_data_values is not None 
                           else list(numerical_values) for i, (column, data_type) 
              in enumerate(num_cols_col_names, range(len(num_cols_col_names)))

    }

    # Generate DataFrame
    generated_df = generate_dataset(num_rows_export,
                                  len(col_names),
                                  random.choice(data_type_selected))

def main():
    st.image('Stream Data Generator.png')

    # Generate Dataset Display Block

    def display_result(df_dict):
        data_display_columns = list(set([key + '\n' for col in df_dict.keys() 
                                          if col != "Text"]) )
        generated_df = generate_dataset(num_rows_export,
                                      len(list(df_dict.keys())[0]), 
                                      str(random.choice(data_type_selected)))

        st.subheader('Generated Dataset Display:')
        with st.expander("Show DataFrame"):
            st.dataframe(generated_df)

    def download_data_file():
        # Generate datasets based on user configuration and types
        df_generate_list = []
        for data_type in data_type_selected:

            df_generate_dict = generate_dataset(num_rows_export,
                                              len(df_generate_list[0].keys()), 
                                              str(data_type).lower())

            df_make_unique_df_dict = {k:v for k, v in zip(df_generate_dict.keys(),
                                                    list(df_generate_dict.values()))}

            if not any(map((lambda x: (x is not None)),
                             [df_make_unique_df_dict[k] and i != data_type 
                              for i, dtype in enumerate(data_type_selected)])
                              df_generate_list)):
                df_generate_list.append(generate_dataset(num_rows_export,
                                                      len(df_generate_list[0].keys()), 
                                                      str(data_type).lower())
                                       )

        # Export to Excel
        export_to_excel_for_buttons = export_data_dict_to_excel()

        st.subheader('Data Generation and Download Options:')
        with st.expander("Select Type of Data Export"):
            for type_of_export, data_generate_list in export_data_dict_to_excel().items():

                if 'CSV' not in type_of_export:
                    if 'SQL' not in type_of_export:
                        buttons_to_download = [
                            "Download XLS File",
                        ]
                        st.download_button(
                            label='Generate & Download',
                            data=generate_sql_query(df_generate_list),
                            filename=f'{type_of_export}_results.csv'
                        )

    if __name__ == '__main__':
        main()

if __name__ == "__main__":
    # Streamlit runs on http://localhost:8501 - use this when running from the command line or kernel in Jupiter
        streamlit.run('main.py', port=8500)
    
