# Reading and processing the dataset
import pandas as pd
import streamlit as st
import re

from summary import summarize_data, verbal_summary, get_exemplary_questions
from llm import use_chatGPT, calc_token_usage

example_query = """Example questions:\n
\t-What is the average value in column X?\n
\t-How many rows in column Y have a value less than 10?\n
\t-Is there a correlation between columns X and Y?"""

def csv_option_select():
    col1, col2 = st.columns([1, 1])
    pattern = r",?\s*([^,\s]+)\s*,?"
    with col1:
        with st.expander("CSV Upload Options"):
            ### Separator ###
            separator = st.selectbox('Separator', [",", ";", "\\t", "\\s", "|", 
                                                                    "Other"])
            if separator == 'Other':
                st.session_state.custom_sep = st.text_input('Custom Separator')
            elif separator == "\\s":
                st.session_state.custom_sep = " "
            elif separator == "\\t":
                st.session_state.custom_sep = "\t"
            else:
                st.session_state.custom_sep = separator

            ### Decimal Separator ###
            st.session_state.decimal = st.selectbox("Decimal Separator", 
                                                                    [".", ","])

            ### Header ###
            header = st.selectbox('Header', ["Yes", "No"])
            if header == "Yes":
                st.session_state.header = st.text_input('Header Row Number')
                if st.session_state.header:
                    try: 
                        st.session_state.header = int(st.session_state.header)-1
                    except: 
                        st.warning("Header row number must be an integer")
            else:
                st.session_state.header = None
                st.session_state.custom_names = st.text_input(
                                    'Custom Column Names (Optional)', 
                                    placeholder="Name1, Name2...")
                if st.session_state.custom_names:
                    st.session_state.custom_names = re.findall(pattern, 
                                                st.session_state.custom_names)
                    st.session_state.header = 0
                    if not st.session_state.custom_names:
                        st.warning("""Make sure to enter the names in the 
                                   correct format: (Name1, Name2...)""")
                    elif len(set(st.session_state.custom_names)) != len(
                                                st.session_state.custom_names):
                        st.warning("Column names must be unique")
                else: 
                    st.session_state.custom_names = None
            
            ### None Type Values ###
            st.session_state.none_val = st.text_input("""Treat values as None 
                                Type (Optional)""", placeholder="NaN1, NaN2...")
            if st.session_state.none_val:
                st.session_state.none_val = re.findall(pattern, 
                                                    st.session_state.none_val)
                if not st.session_state.none_val:
                    st.warning("""Make sure to enter the values in the correct 
                                                format: (NaN1, NaN2...)""")
            option_use = st.checkbox("Apply options on upload")
    with col2:
        st.empty()
    return option_use

def file_manager(test_data):
    if not st.session_state.test_data:
        file_uploader = st.file_uploader("Upload your CSV file", type="csv")
        if not st.session_state.data_uploaded:
            if st.button("Use test data"):
                file_uploader = test_data
                st.session_state.test_data = True
    if st.session_state.test_data:
        file_uploader = test_data
        if st.button("Remove test data"):
            st.session_state.test_data = False
            file_uploader = st.file_uploader("Upload your CSV file", type="csv")
            st.button("Use test data")
    if file_uploader is None:
        st.session_state.data_uploaded = False
    
    return file_uploader

def upload_manager(file_uploader, option_summary=False, option_use=False):
    try: 
        file_upload(file_uploader, option_summary, option_use)
        if st.session_state.test_data: 
            st.toast("Test data loaded successfully")
        else:
            st.toast("Upload successful")
    except Exception as e: 
        st.error(f"Error processing the data. Please try again.\nDetails: {e}")

def file_upload(file_uploader, option_summary, option_use):
    if option_use and not st.session_state.test_data:
        st.session_state.data = pd.read_csv(file_uploader, 
                                sep = st.session_state.custom_sep, 
                                decimal = st.session_state.decimal, 
                                header = st.session_state.header, 
                                na_values = st.session_state.none_val,
                                names = st.session_state.custom_names)
    else:    
        st.session_state.data = pd.read_csv(file_uploader)
    
    st.session_state.df = pd.DataFrame(st.session_state.data)
    st.session_state.messages = []
    st.session_state.messages1 = []
    calc_token_usage()
    if not st.session_state.data.empty:
        st.session_state.data_summary = summarize_data(st.session_state.data) 
        st.session_state.data_uploaded = True
    else:
        st.error("Data cannot be processed")
    if not st.session_state.data.empty:
        with st.spinner("Analyzing data..."):    
            st.session_state.exemplary_questions = None
            streamed_data = use_chatGPT(st.session_state.data_summary, 
                                                        option_summary) 
            try:  
                st.session_state.verbal_summary = verbal_summary(streamed_data,
                                                                option_summary)
                st.session_state.exemplary_questions = get_exemplary_questions(
                                                st.session_state.verbal_summary)
            except:
                st.session_state.exemplary_questions = example_query
            

def filter_data(df, categories):
    
    for category in categories:
        st.sidebar.write(f"Filter for {category}")
        filter_option = st.sidebar.selectbox(
            f"Filter type for {category}",
            ["No Filter", "Less than", "Greater than", "Equal to"],
            key=f"filter_option_{category}"
        )
        filter_value = st.sidebar.number_input(
            f"Filter value for {category}",
            value=0,
            key=f"filter_value_{category}"
        )
        
        if filter_option == "Less than":
            df = df[df[category] < filter_value]
        elif filter_option == "Greater than":
            df = df[df[category] > filter_value]
        elif filter_option == "Equal to":
            df = df[df[category] == filter_value]

    return df

def get_user_selection(df, multicat=False, subcat=True):
    categories = [col for col in df.columns]
    if multicat:
        selected_category = st.sidebar.multiselect(
                                "Select one or more categories:", 
                                options=categories,
                                default=None
                                )
        
    else:
        selected_category = st.sidebar.selectbox("Select a category:", 
                                                            categories)

    if subcat:
        other_columns = [col for col in df.columns 
                                    if col not in selected_category]
        selected_subcategories = st.sidebar.multiselect(
                                        "Select one or more subcategories:", 
                                        options=other_columns, default=None
                                        )
    else: 
        selected_subcategories = None

    return selected_category, selected_subcategories
