# Einlesesn und Verarbeiten des Datensatzes
import pandas as pd
import streamlit as st
import re

from summary import summarize_data, verbal_summary
from llm import use_chatGPT, calc_token_usage

def csv_option_select():
    col1, col2 = st.columns([1, 1])
    pattern = r",?\s*([^,\s]+)\s*,?"
    with col1:
        with st.expander("CSV Upload Optionen"):
            ###Seperator####
            seperator = st.selectbox('Seperator', [",", ";", "\\t", "\\s", "|", "Anderer"])
            if seperator == 'Anderer':
                st.session_state.custom_sep = st.text_input('Benutzerdefiniertes Trennzeichen')
            elif seperator == "\\s":
                st.session_state.custom_sep = " "
            elif seperator == "\\t":
                st.session_state.custom_sep = "\t"
            else:
                st.session_state.custom_sep = seperator

            ###Dezimal Trennzeichen####
            st.session_state.decimal = st.selectbox("Dezimal Trennzeichen", [".", ","])

            ###Header###
            header = st.selectbox('Header', ["Ja", "Nein"])
            if header == "Ja":
                st.session_state.header = st.text_input('Zeilennummer des Headers')
                if st.session_state.header:
                    try: st.session_state.header = int(st.session_state.header) - 1
                    except: st.warning("Zeilennummer des Headers muss ganzzahlig sein")
            else:
                st.session_state.header = None
                st.session_state.custom_names = st.text_input(
                                    'Benutzerdefinierte Spaltennamen (Optional)', 
                                    placeholder="Name1, Name2...")
                if st.session_state.custom_names:
                    st.session_state.custom_names = re.findall(pattern, st.session_state.custom_names)
                    st.session_state.header = 0
                    if not st.session_state.custom_names:
                        st.warning("Achte auf das korrekte Eingabeformat: (Name1, Name2...)")
                    elif len(set(st.session_state.custom_names)) != len(st.session_state.custom_names):
                        st.warning("Spaltennamen müssen einzigartig sein")
                else: 
                    st.session_state.custom_names = None
            
            ###None Type Werte###
            st.session_state.none_val = st.text_input('Werte als None - Type behandeln (Optional)', placeholder="NaN1, NaN2...")
            if st.session_state.none_val:
                st.session_state.none_val = re.findall(pattern, st.session_state.none_val)
                if not st.session_state.none_val:
                    st.warning("Achte auf das korrekte Eingabeformat: (NaN1, NaN2...)")
            option_use = st.checkbox("Auswahl beim Upload anwenden")
    with col2:
        st.empty()
    return option_use

def file_manager(test_data):
    if not st.session_state.test_data:
        file_uploader = st.file_uploader("Lade deine CSV Datei hoch", type="csv")
        if not st.session_state.data_uploaded:
            if st.button("Testdaten verwenden"):
                file_uploader = test_data
                st.session_state.test_data = True
    if st.session_state.test_data:
        file_uploader = test_data
        if st.button("Testdaten entfernen"):
            st.session_state.test_data = False
            file_uploader = st.file_uploader("Lade deine CSV Datei hoch", type="csv")
            st.button("Testdaten verwenden")
    if file_uploader is None:
        st.session_state.data_uploaded = False
    
    return file_uploader

def upload_manager(file_uploader, option_summary=False, option_use=False):
    try: 
        file_upload(file_uploader, option_summary, option_use)
        if st.session_state.test_data: 
            st.toast("Testdaten erfolgreich geladen")
        else:
            st.toast("Upload erfolgreich")
    except: 
        st.error("Fehler beim Upload der Daten. Versuche es erneut.")

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
        st.error("Daten können nicht verarbeitet werden")
    if option_summary and st.session_state.data:
        with st.spinner("Daten werden analysiert..."):    
            streamed_data = use_chatGPT(st.session_state.data_summary) 
            st.session_state.verbal_summary = verbal_summary(streamed_data)

def filter_data(df, categories):
    
    for kategorie in categories:
        st.sidebar.write(f"Filter für {kategorie}")
        filter_option = st.sidebar.selectbox(
            f"Filtertyp für {kategorie}",
            ["Keine Filter", "Kleiner als", "Größer als", "Gleich"],
            key=f"filter_option_{kategorie}"
        )
        filter_value = st.sidebar.number_input(
            f"Filterwert für {kategorie}",
            value=0,
            key=f"filter_value_{kategorie}"
        )
        
        if filter_option == "Kleiner als":
            df = df[df[kategorie] < filter_value]
        elif filter_option == "Größer als":
            df = df[df[kategorie] > filter_value]
        elif filter_option == "Gleich":
            df = df[df[kategorie] == filter_value]

    return df

def get_user_selection(df, multicat=False, subcat=True):
    categories = [col for col in df.columns]
    if multicat:
        selected_category = st.sidebar.multiselect(
                                "Wähle eine oder mehrere Kategorien:", 
                                options=categories,
                                default=None
                                )
        
    else:
        selected_category = st.sidebar.selectbox("Wähle eine Kategorie:", categories)

    if subcat:
        other_columns = [col for col in df.columns if col not in selected_category]
        selected_subcategories = st.sidebar.multiselect(
                                        "Wähle eine oder mehrere Nebenkategorien:", 
                                        options=other_columns, default=None
                                        )
    else: 
        selected_subcategories = None

    return selected_category, selected_subcategories
