import streamlit as st 

#st.session_state wird verwendet, damit bestimmte code Abschnitte nur ein einziges
#mal ausgeführt werden und um variablen über sessions hinweg zu speichern.

def initialize_variables():
     #upload Optionen
    #_____________________________________#  
    if "custom_sep" not in st.session_state:
        st.session_state.custom_sep = None
    if "decimal" not in st.session_state:
        st.session_state.decimal = None
    if "header" not in st.session_state:
        st.session_state.header = None
    if "none_val" not in st.session_state:
        st.session_state.none_val = None
    if "custom_names" not in st.session_state:
        st.session_state.custom_names = None
    #_____________________________________#    
    #Datensatz
    #_____________________________________#  
    if 'test_data' not in st.session_state:
        st.session_state.test_data = None
    if 'data' not in st.session_state:
        st.session_state.data = None
    if 'df' not in st.session_state:
        st.session_state.df = None
    if 'df_filtered' not in st.session_state:
        st.session_state.df_filtered = None
    if 'data_uploaded' not in st.session_state:
        st.session_state.data_uploaded = False
    #_____________________________________#  
    if 'num_tokens' not in st.session_state: 
        st.session_state.num_tokens = None
    if 'token_usage_percent' not in st.session_state: 
        st.session_state.token_usage_percent = None
    if 'verbal_summary' not in st.session_state:
        st.session_state.verbal_summary = None
    if 'exemplary_questions' not in st.session_state:
        st.session_state.exemplary_questions = None
    if 'data_summary' not in st.session_state:
        st.session_state.data_summary = None
    if 'tab_visited' not in st.session_state:
        st.session_state.tab_visited = False
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "messages1" not in st.session_state:
        st.session_state.messages1 = []
