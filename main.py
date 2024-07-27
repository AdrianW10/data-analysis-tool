#### Main Program to Run ####

###### Import ######
import streamlit as st 
st.set_page_config(layout="wide", page_title="Data Analysis", 
                   page_icon="favicon.ico")

###### Import Functions from Files ######
from data_processor import filter_data, get_user_selection, upload_manager, file_manager, csv_option_select
from llm import chatbot
from interactive_plot import interactive_plot
from session_variables import initialize_variables

###########################################################
########## Initialization and Prerequisites ###############
###########################################################

if "initialized" not in st.session_state:
    st.session_state.initialized = None

if not st.session_state.initialized:
    initialize_variables()
    st.session_state.initialized = True

test_data = "titanic.csv"

######################
## Application ##
######################
menu = st.sidebar.selectbox("Choose an Option", ["Home", "Data Analysis", 
                                "Interactive Data Visualization"])
st.sidebar.button("Refresh")

######### Home #########
if menu == "Home":
    st.image("header.jpeg", use_column_width=True)    
    
    if not st.session_state.data_uploaded:
        option_use = csv_option_select()
   
    file_uploader = file_manager(test_data) 
        
    if not st.session_state.data_uploaded:
        option_summary = st.checkbox("Generate Verbal Summary")
    else: 
        option_summary = False
        
    if file_uploader is not None:
        if not st.session_state.data_uploaded:
            upload_manager(file_uploader, option_summary, option_use)
        if st.session_state.verbal_summary and st.session_state.tab_visited:
            with st.expander("View Verbal Summary"):
                st.write(st.session_state.verbal_summary)
        st.write(f"Number of Tokens: ≈ {st.session_state.num_tokens}")
        st.write(f"Maximum Tokens: {8192}")
        try: st.progress(st.session_state.token_usage_percent)
        except: st.error("Token limit exceeded, no requests to the AI possible.")
        st.write(f"Token Usage: {st.session_state.token_usage_percent}%")
        st.info("Overview of your Data")
        if not st.session_state.data.empty:
            st.write(st.session_state.data.head(10))
        else:
            st.error("Data cannot be processed")
        
        
######### Data Analysis #########                                       
elif menu == "Data Analysis":
    st.session_state.tab_visited = True
    st.title("AI-Powered Data Analysis")
    if not st.session_state.data_uploaded:
        option_use = csv_option_select()
    file_uploader = file_manager(test_data)
    if file_uploader is not None:
        if not st.session_state.data_uploaded:
            upload_manager(file_uploader)
        if not st.session_state.data.empty:
            with st.expander("Descriptive Statistics of Numeric Data"):
                st.write(st.session_state.df.describe())
            with st.expander("View Summary"): 
                    st.text(st.session_state.data_summary)
            option_analysis = st.sidebar.radio("How would you like to proceed?",
                                    ["Use entire dataset", 
                                    "Filter data manually first"])
            if option_analysis == "Use entire dataset":
                st.session_state.df_filtered = None
                option_answer = st.checkbox("Show Thought Process")
                option_plot = st.checkbox("Create Chart")
                chatbot(option_answer, option_plot, st.session_state.messages)
            else: 
                categories, current_selection = get_user_selection(
                                                st.session_state.df, 
                                                multicat=True, 
                                                subcat=False,
                                                )
                st.session_state.df_filtered = filter_data(
                    st.session_state.df[categories], categories)
                
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.info("Filtered Dataset")
                    st.write(st.session_state.df_filtered)
                with col2:
                    st.info("Learn more about your filtered data")
                    option_answer = st.checkbox("Show Thought Process")
                    option_plot = st.checkbox("Create Chart")
                    chatbot(option_answer, option_plot, 
                            st.session_state.messages1)
        else:
            st.error("Data cannot be processed")
           
######### Interactive Data Visualization #########  
                
elif menu == "Interactive Data Visualization":
    st.session_state.tab_visited = True
    st.title("Interactive Data Visualization")
    if not st.session_state.data_uploaded:
        option_use = csv_option_select()
    file_uploader = file_manager(test_data)
    if file_uploader is not None:
        if not st.session_state.data_uploaded:
            upload_manager(file_uploader)
        if not st.session_state.data.empty:
            option_analysis = st.sidebar.radio("How would you like to proceed?",
                                    ["Use entire dataset", 
                                    "Filter data manually first"])
            if option_analysis == "Use entire dataset":
                st.session_state.df_filtered = None
                with st.expander("View Summary"): 
                    st.text(st.session_state.data_summary)
                interactive_plot(st.session_state.df)
            else: 
                categories, current_selection = get_user_selection(
                                                st.session_state.df, 
                                                multicat=True, 
                                                subcat=False,
                                                )
                st.session_state.df_filtered = filter_data(
                    st.session_state.df[categories], categories)
                interactive_plot(st.session_state.df_filtered, True)
        else:
            st.error("Data cannot be processed")

######### Info #########  

for _ in range(49): 
    st.sidebar.write("")

with st.sidebar.empty():
    st.markdown("""<hr>""", unsafe_allow_html=True)
    st.markdown("""<small>[AI Analysis Streamlit App](https://github.com/AdrianW10/data-analysis-tool.git)  | Jul 2024 | [Adrian Wagner](https://github.com/AdrianW10)</small>""", unsafe_allow_html=True)
