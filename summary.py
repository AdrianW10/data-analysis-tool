import streamlit as st
import re

# Method to create a comprehensive summary of the data.
def summarize_data(data):
    
    # Descriptive statistics for numerical data
    numerical_summary = data.describe().transpose().to_string()
    
    # Analysis of categorical data
    categorical_columns = data.select_dtypes(include=["object", 
                                                      "category"]).columns
    categorical_summary = ""
    for col in categorical_columns:
        val_counts = data[col].value_counts()
        if len(val_counts) > 100:
            continue
        categorical_summary += f"""\n{col} distribution:
                                                \n{val_counts.to_string()}\n"""
    
    # Check for missing data
    missing_data_summary = data.isnull().sum().to_string()
    
    # Compile summary text
    summary=f"Descriptive statistics for numerical data:\n{numerical_summary}\n"
    summary+=f"Categorical data analysis:\n{categorical_summary}\n"
    summary+=f"Missing data in each column:\n{missing_data_summary}"
    
    return summary 

def verbal_summary(streamed_data, option_summary):
    if option_summary:
        verbal_summary = st.write_stream(streamed_data)
    else:
        verbal_summary = "".join(choice.message.content for choice in 
                                                        streamed_data.choices)
    return verbal_summary

def get_exemplary_questions(verbal_summary):
    qestions = re.search(r"(Exemplary questions:\n.*)",verbal_summary,re.DOTALL)
    return qestions.group(1) if qestions else None
