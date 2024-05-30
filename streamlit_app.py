import streamlit as st 
import pandas as pd


# function applies filters and counts non blank records for each variable
def filter_count(df, cols, variables):
    filtered_df = df.copy()
    for column, values in cols.items():  # iterates through each filter
        filtered_df = filtered_df[filtered_df[column].isin(values)]  # applies filter to data
    
    # count non-blank records for each variable
    non_blank_counts = {var: filtered_df[var].notna().sum() for var in variables} 
    
    return non_blank_counts 

# streamlit title and subtitle
st.title("ACL Dashboard")  # title
st.write("Apply filters to see non-blank record counts for variables.")

# upload dataset in pandas
data = pd.read_excel("Dashboard Headers.xlsx")

# defining variables to count non blank records
variables = [
    "insurance_dashboard_use", "ikdc", "pedi_ikdc", "marx", "pedi_fabs", "koos_pain", 
    "koos_sx", "koos_adl", "koos_sport", "koos_qol", "acl_rsi", "tsk", "rsi_score", 
    "rsi_emo", "rsi_con", "sh_lsi", "th_lsi", "ch_lsi", "lsi_ext_mvic_90", 
    "lsi_ext_mvic_60", "lsi_flex_mvic_60", "lsi_ext_isok_60", "lsi_flex_isok_60", 
    "lsi_ext_isok_90", "lsi_flex_isok_90", "lsi_ext_isok_180", "lsi_flex_isok_180", 
    "rts", "reinjury"]

# ask for filter criteria
st.subheader("Enter filter criteria:")
cols = {}

# filters with subgroups
filter_columns = {
    "sex_dashboard": ["Female", "Male"],
    "age_group_dashboard_use": ["12 to 14 years", "15 to 17 years", "18 to 20 years", "21 to 25 years", "26 to 34 years"],
    "graft_dashboard2": ["Allograft", "BTB autograft", "HS autograft", "Other", "QT autograft"],
    "prior_aclr": ["Yes", "No"],
    "tss_dashboard": ["13 to 24 months", "8 to 12 months", "5 to 7 months", "3 to 4 months"]
}

# make drop down selections for each filter
for column, options in filter_columns.items():
    selected_values = st.multiselect(f"Select value for '{column}'", options) 
    if selected_values:
        cols[column] = selected_values  # Add selected values to the filter criteria

# call function 
if st.button("Apply Filters"): # adding button
    result_counts = filter_count(df=data, cols=cols, variables=variables)
    
    # print results
    st.write("Counts of Non-Blank Records for Variables:")
    for var, count in result_counts.items():
        st.write(f"{var}: {count}")

# add a button to clear all filters?
