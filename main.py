#### Haputprogramm zur Ausführung ####

###### Import ######
import streamlit as st 
st.set_page_config(layout="wide", page_title="Data Analysis", 
                   page_icon="favicon.ico")

###### Import von Funktionen aus Dateien ######
from data_processor import filter_data, get_user_selection, upload_manager, file_manager, csv_option_select
from llm import chatbot
from interactive_plot import interactive_plot
from session_variables import initialize_variables

###########################################################
########## Initialisierung und Vorraussetzungen ###########
###########################################################
if "initialized" not in st.session_state:
    st.session_state.initialized = None

if not st.session_state.initialized:
    initialize_variables()
    st.session_state.initialized = True

test_data = "titanic.csv"

######################
## Anwendung selbst ##
######################
menu = st.sidebar.selectbox("Wähle eine Option", ["Startseite", "Datenanalyse", 
                                "Interaktive Datenvisualisierung"])
st.sidebar.button("Refresh")

######### Startseite #########
if menu == "Startseite":
    st.image("header.jpeg", use_column_width=True)    
    
    if not st.session_state.data_uploaded:
        option_use = csv_option_select()
   
    file_uploader = file_manager(test_data) 
        
    if not st.session_state.data_uploaded:
        option_summary = st.checkbox("Verbale Zusammenfassung erzeugen")
    else: 
        option_summary = False
        
    if file_uploader is not None:
        if not st.session_state.data_uploaded:
            upload_manager(file_uploader, option_summary, option_use)
        if st.session_state.verbal_summary and st.session_state.tab_visited:
            with st.expander("Verbale Zusammenfassung ansehen"):
                st.write(st.session_state.verbal_summary)
        st.write(f"Anzahl der Tokens: ≈ {st.session_state.num_tokens}")
        st.write(f"Maximale Tokens: {8192}")
        try: st.progress(st.session_state.token_usage_percent)
        except: st.error("Tokenlimit überschritten, keine Anfragen an die KI möglich.")
        st.write(f"Token-Verbrauch: {st.session_state.token_usage_percent}%")
        st.info("Übersicht über deine Daten")
        if not st.session_state.data.empty:
            st.write(st.session_state.data.head(10))
        else:
            st.error("Daten können nicht verarbeitet werden")
        
        
######### Datenanalyse #########                                       
elif menu == "Datenanalyse":
    st.session_state.tab_visited = True
    st.title("Lasse deine Daten automatisch analysieren")
    if not st.session_state.data_uploaded:
        option_use = csv_option_select()
    file_uploader = file_manager(test_data)
    if file_uploader is not None:
        if not st.session_state.data_uploaded:
            upload_manager(file_uploader)
        if not st.session_state.data.empty:
            with st.expander("Deskriptive Statistik der numerischen Daten"):
                st.write(st.session_state.df.describe())
            with st.expander("Zusammenfassung ansehen"): 
                    st.text(st.session_state.data_summary)
            option_analysis = st.sidebar.radio("Wie möchtest du vorgehen?",
                                    ["Kompletten Datensatz verwenden", 
                                    "Daten erst manuell filtern"])
            if option_analysis == "Kompletten Datensatz verwenden":
                st.session_state.df_filtered = None
                option_answer = st.checkbox("Gedankenprozess anzeigen")
                option_plot = st.checkbox("Grafik erstellen")
                chatbot(option_answer, option_plot, st.session_state.messages)
            else: 
                kategorien, current_selection = get_user_selection(
                                                st.session_state.df, 
                                                multicat=True, 
                                                subcat=False,
                                                )
                st.session_state.df_filtered = filter_data(st.session_state.df[kategorien], kategorien)
                
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.info("Gefilterter Datensatz")
                    st.write(st.session_state.df_filtered)
                with col2:
                    st.info("Erfahre mehr über deine gefilterten Daten")
                    option_answer = st.checkbox("Gedankenprozess anzeigen")
                    option_plot = st.checkbox("Grafik erstellen")
                    chatbot(option_answer, option_plot, st.session_state.messages1)
        else:
            st.error("Daten können nicht verarbeitet werden")
           
######### Interaktive Datenvisualisierung #########  
                
elif menu == "Interaktive Datenvisualisierung":
    st.session_state.tab_visited = True
    st.title("Interaktive Datenvisualisierung")
    if not st.session_state.data_uploaded:
        option_use = csv_option_select()
    file_uploader = file_manager(test_data)
    if file_uploader is not None:
        if not st.session_state.data_uploaded:
            upload_manager(file_uploader)
        if not st.session_state.data.empty:
            option_analysis = st.sidebar.radio("Wie möchtest du vorgehen?",
                                    ["Kompletten Datensatz verwenden", 
                                    "Daten erst manuell filtern"])
            if option_analysis == "Kompletten Datensatz verwenden":
                st.session_state.df_filtered = None
                interactive_plot(st.session_state.df)
            else: 
                kategorien, current_selection = get_user_selection(
                                                st.session_state.df, 
                                                multicat=True, 
                                                subcat=False,
                                                )
                st.session_state.df_filtered = filter_data(st.session_state.df[kategorien], kategorien)
                interactive_plot(st.session_state.df_filtered, True)
        else:
            st.error("Daten können nicht verarbeitet werden")
    

