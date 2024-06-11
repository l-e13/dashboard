import streamlit as st 
import pandas as pd

# Streamlit title and subtitle
st.title("ACL Dashboard")  # Title
st.write("Apply filters to see non-blank record counts for variables and preview the dataset.")

# Upload dataset in pandas
data = pd.read_excel("PRODRSOMDashboardDat_DATA_2024-06-04_1845.xlsx")

# Function to fill missing values for each record_id
def propagate_values(df, columns):
    for column in columns:
        df[column] = df.groupby('record_id')[column].ffill().bfill()
    return df

# Propagate values for 'sex_dashboard', 'graft_dashboard2', and 'prior_aclr'
data = propagate_values(data, ['sex_dashboard', 'graft_dashboard2', 'prior_aclr'])

# Function applies filters and counts non-blank records for each variable
def filter_count(df, cols, variables):
    filtered_df = df.copy()
    for column, values in cols.items():  # Iterates through each filter
        filtered_df = filtered_df[filtered_df[column].isin(values)]  # Applies filter to data
    
    # Count non-blank records for each variable
    non_blank_counts = {var: filtered_df[var].notna().sum() for var in variables} 
    
    return non_blank_counts, filtered_df

# Define variables to count non-blank records
variables = [
    "insurance_dashboard_use", "ikdc", "pedi_ikdc", "marx", "pedi_fabs", "koos_pain", 
    "koos_sx", "koos_adl", "koos_sport", "koos_qol", "acl_rsi", "tsk", "rsi_score", 
    "rsi_emo", "rsi_con", "sh_lsi", "th_lsi", "ch_lsi", "lsi_ext_mvic_90", 
    "lsi_ext_mvic_60", "lsi_flex_mvic_60", "lsi_ext_isok_60", "lsi_flex_isok_60", 
    "lsi_ext_isok_90", "lsi_flex_isok_90", "lsi_ext_isok_180", "lsi_flex_isok_180", 
    "rts", "reinjury"]

# Ask for filter criteria
st.subheader("Enter filter criteria:")
cols = {}

# Filters with subgroups
filter_columns = {
    "sex_dashboard": ["Female", "Male"],
    "age_group_dashboard_use": ["12 to 14 years", "15 to 17 years", "18 to 20 years", "21 to 25 years", "26 to 34 years"],
    "graft_dashboard2": ["Allograft", "BTB autograft", "HS autograft", "Other", "QT autograft"],
    "prior_aclr": ["Yes", "No"],
    "tss_dashboard": ["13 to 24 months", "8 to 12 months", "5 to 7 months", "3 to 4 months"]
}

# Make drop down selections for each filter
for column, options in filter_columns.items():
    if column == "prior_aclr":
        selected_values = st.multiselect(f"Select value for '{column}'", options) 
        selected_values = [1 if v == "Yes" else 0 for v in selected_values]  # Convert Yes/No to 1/0
    else:
        selected_values = st.multiselect(f"Select value for '{column}'", options)
    
    if selected_values:
        cols[column] = selected_values  # Add selected values to the filter criteria

# Call function 
if st.button("Apply Filters"):  # Adding button
    result_counts, filtered_data = filter_count(df=data, cols=cols, variables=variables)
    
    # Print results
    st.write("Counts of Non-Blank Records for Variables:")
    for var, count in result_counts.items():
        st.write(f"{var}: {count}")
    
