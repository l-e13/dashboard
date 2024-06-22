import streamlit as st
import pandas as pd
import hmac

# Password protection function
def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False

if not check_password():
    st.stop()  # Do not continue if check_password is not True.

# Streamlit title and subtitle
st.title("ACL Dashboard")  # Title
st.write("Apply filters to see non-blank record counts for variables.")

# Upload dataset
data = pd.read_excel("PRODRSOMDashboardDat_DATA_2024-06-04_1845.xlsx")

# Function to fill missing values for each record id
def autofill(df, columns):
    for column in columns:
        df[column] = df.groupby('record_id')[column].ffill().bfill()
    return df

# Propagate values for sex_dashboard, graft_dashboard2, and prior_aclr so they are consistent throughout the record id
data = autofill(data, ['sex_dashboard', 'graft_dashboard2', 'prior_aclr'])

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
    "graft_dashboard2": ["Allograft", "BTB autograft", "HS autograft", "Other", "QT autograft"],
    "prior_aclr": ["Yes", "No"]
}

# Make drop down selections for each filter
for column, options in filter_columns.items():
    if column == "prior_aclr":
        selected_values = st.multiselect(f"Select value for '{column}'", options) 
        selected_values = [1 if v == "Yes" else 0 for v in selected_values]  # Converting yes/no to 1/0
    else:
        selected_values = st.multiselect(f"Select value for '{column}'", options)
        
    if selected_values:
        cols[column] = selected_values  

# Add age range slider
age_min = int(data['age'].min())
age_max = int(data['age'].max())
age_range = st.slider("Select age range", min_value=age_min, max_value=age_max, value=(age_min, age_max))
cols['age'] = list(range(age_range[0], age_range[1] + 1))

# Add time since surgery (tss) range slider
tss_min = int(data['tss'].min())
tss_max = int(data['tss'].max())
tss_range = st.slider("Select time since surgery range (months)", min_value=tss_min, max_value=tss_max, value=(tss_min, tss_max))
cols['tss'] = list(range(tss_range[0], tss_range[1] + 1))

# Call the function 
if st.button("Apply Filters"):  # Adding button
    result_counts, filtered_data = filter_count(df=data, cols=cols, variables=variables)
        
    # Print results
    st.write("Counts of Non-Blank Records for Variables:")
    for var, count in result_counts.items():
        st.write(f"{var}: {count}")
