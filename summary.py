import streamlit as st


# Methode, die eine umfassende Zusammenfassung der Daten erstellt.
def summarize_data(data):
    
    # Deskriptive Statistik für numerische Daten
    numerical_summary = data.describe().transpose().to_string()
    
    # Analyse kategorialer Daten
    categorical_columns = data.select_dtypes(include=['object', 'category']).columns
    categorical_summary = ""
    for col in categorical_columns:
        val_counts = data[col].value_counts()
        if len(val_counts) > 100:
            continue
        categorical_summary += f"\n{col} Verteilung:\n{val_counts.to_string()}\n"
    
    # Überprüfung auf fehlende Daten
    missing_data_summary = data.isnull().sum().to_string()
    
    # Zusammenfassungstext zusammenstellen
    summary = f"Deskriptive Statistik der numerischen Daten:\n{numerical_summary}\n"
    summary += f"Kategoriale Datenanalyse:\n{categorical_summary}\n"
    summary += f"Fehlende Daten in jeder Spalte:\n{missing_data_summary}"
    
    return summary 

def verbal_summary(streamed_data):
    verbal_summary = st.write_stream(streamed_data)
    return verbal_summary
