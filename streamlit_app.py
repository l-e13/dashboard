import streamlit as st
import pandas as pd
import hmac

# password protection function
def check_password():
    """returns `true` if the user had the correct password."""

    def password_entered():
        """checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store the password.
        else:
            st.session_state["password_correct"] = False

    # return true if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # show input for password.
    st.text_input(
        "password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 password incorrect")
    return False

if not check_password():
    st.stop()  # do not continue if check_password is not true.

# streamlit title and subtitle
st.title("ACL Dashboard ")  # title
st.write("Apply filters to see non-blank record counts for variables.")

# upload dataset
data = pd.read_excel("PRODRSOMDashboardDat_DATA_2024-06-04_1845.xlsx")


# function to fill missing values for each record id
def autofill(df, columns):
    for column in columns:
        df[column] = df.groupby('record_id')[column].ffill().bfill()
    return df

# propagate values for sex_dashboard, graft_dashboard2, and prior_aclr so they are consistent throughout the record id
data = autofill(data, ['sex_dashboard', 'graft_dashboard2', 'prior_aclr'])

# function applies filters and counts non-blank records for each variable
def filter_count(df, cols, variables):
    filtered_df = df.copy()
    for column, values in cols.items():  # iterates through each filter
        filtered_df = filtered_df[filtered_df[column].isin(values)]  # applies filter to data
        
    # count non-blank records for each variable
    non_blank_counts = {var: filtered_df[var].notna().sum() for var in variables} 
        
    return non_blank_counts, filtered_df

# define variables to count non-blank records
variables = [
    "insurance_dashboard_use", "ikdc", "pedi_ikdc", "marx", "pedi_fabs", "koos_pain", 
    "koos_sx", "koos_adl", "koos_sport", "koos_qol", "acl_rsi", "tsk", "rsi_score", 
    "rsi_emo", "rsi_con", "sh_lsi", "th_lsi", "ch_lsi", "lsi_ext_mvic_90", 
    "lsi_ext_mvic_60", "lsi_flex_mvic_60", "lsi_ext_isok_60", "lsi_flex_isok_60", 
    "lsi_ext_isok_90", "lsi_flex_isok_90", "lsi_ext_isok_180", "lsi_flex_isok_180", 
    "rts", "reinjury"]

# ask for filter criteria
st.subheader("enter filter criteria:")
cols = {}

# filters with subgroups
filter_columns = {
    "sex_dashboard": ["female", "male"],
    "graft_dashboard2": ["allograft", "btb autograft", "hs autograft", "other", "qt autograft"],
    "prior_aclr": ["yes", "no"]
}

# make drop down selections for each filter
for column, options in filter_columns.items():
    if column == "prior_aclr":
        selected_values = st.multiselect(f"select value for '{column}'", options) 
        selected_values = [1 if v == "yes" else 0 for v in selected_values]  # converting yes/no to 1/0
    else:
        selected_values = st.multiselect(f"select value for '{column}'", options)
        
    if selected_values:
        cols[column] = selected_values  

# add age range slider
age_min = int(data['age'].min())
age_max = int(data['age'].max())
age_range = st.slider("select age range", min_value=age_min, max_value=age_max, value=(age_min, age_max))
cols['age'] = list(range(age_range[0], age_range[1] + 1))


# call the function 
if st.button("apply filters"):  # adding button
    result_counts, filtered_data = filter_count(df=data, cols=cols, variables=variables)
        
    # print results
    st.write("counts of non-blank records for variables:")
    for var, count in result_counts.items():
        st.write(f"{var}: {count}")
