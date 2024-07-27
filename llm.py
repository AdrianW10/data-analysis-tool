import streamlit as st
from openai import OpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import tiktoken
import re
from thought_process import CapturingThoughtProcess
# Client muss hier nochmal zusätzlich definiert werden
load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
chat = ChatOpenAI(model_name="gpt-4",temperature=0.0)
example_query = """Frage zum Beispiel:\n
\t-Was ist der durchschnittliche Wert in Spalte X?\n
\t-Wie viele Zeilen in Spalte Y haben einen kleineren Wert als 10?\n
\t-Gibt es einen Zusammenhang zwischen Spalten X und Y?
"""

def use_chatGPT(query):

    template = {
                "role": "system", "content": """Sie sind ein hilfreiches Modell, 
                das Fragen zu einer CSV-Datei beantwortet, basierend auf den 
                gegebenen Dateninformationen. """, 
                
                "role": "user", "content": """Bitte sprechen Sie mich mit Adrian 
                an und duzen Sie mich.\n\n"""
                
            }

    template["content"] += query
    
    response = client.chat.completions.create(
        messages=[template],
        model="gpt-4",
        stream=True,
            )
    return response

def chatbot(option_answer, option_plot, chat_history):
    # Abbildung der Chathistorie (falls vorhanden) 
    for message in chat_history:
        with st.chat_message(message["role"]):
            if re.search(r"import", message["content"]):
                try: exec(message["content"]) 
                except: pass
            else:
                st.markdown(message["content"])
    
    if prompt := st.chat_input("Sende eine Frage"):
        chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
    
    if option_answer and option_plot:
        st.warning("Gedankenprozess kann nicht in Verbindung mit Grafiken angezeigt werden.")
    
    if prompt is None and len(chat_history) == 0:
        with st.chat_message("assistant"):
            st.write("Was möchtest du zu den Daten du wissen?\n\n" + example_query)
    elif prompt is None:
        with st.chat_message("assistant"):
            st.write("Was möchtest du zu den Daten du wissen?")

    else:
        with st.spinner("Daten werden analysiert..."):
            with st.chat_message("assistant"):
                response = response_manager(option_answer, option_plot, prompt)
                if not option_plot: 
                    st.write(response)
                chat_history.append({"role": "assistant", "content": response})

def response_manager(option_answer, option_plot, prompt):
    if not option_answer and not option_plot:
        response = analyse_csv_data(prompt)
    elif option_answer and not option_plot:  # Wenn der Gedankenprozess angezeigt werden soll...
        with CapturingThoughtProcess() as output: # Gedankenprozess wird in einer Instanz der Klasse CapturingThoughtProcess gespeichert 
            response = analyse_csv_data(prompt)
        output.display_text() # Ausgabe des Gedankenprozesses
    elif option_plot: # Wenn diese Option ausgewählt ist: Spezielle Anweisung, die code für eine Grafik fordert
        prompt += """\nBitte gebe als Antwort 
        lediglich den code, der die Grafik erstellt. Ersetze 
        dabei 'df' durch 'st.session_state.df' und 'plt.show()'
        durch 'st.pyplot(plt, clear_figure=True)' und stelle 
        die figsize des Plots auf (10,5)."""
        
        code = analyse_csv_data(prompt)
        fixed_code = re.search(r"```python(.*)```", code, re.DOTALL) # Code für Grafik wird bereinigt
        try: response = fixed_code.group(1); exec(fixed_code.group(1)) # Code für Grafik wird ausgeführt
        except: st.error("Etwas ist schief gelaufen, probiere es nochmal.")
    return response

# Methode, um einen Input (query) an ChatGPT mittels langchain Schnittstelle zu übergeben 
def analyse_csv_data(query):
    
    agent = create_pandas_dataframe_agent(chat, 
        st.session_state.df if st.session_state.df_filtered is None 
        else st.session_state.df_filtered, 
        verbose=True,
        ) 
    response = agent.run("Bitte beantworte folgende Frage auf deutsch: " + query)
    
    return response

def calc_token_usage(model="gpt-4"):
    df_string = st.session_state.df.head(6).to_string(index=False)
    query = """Dies ist eine Beispielanfrage, die von der Anzahl der Tokens 
                    ungefähr einer durchschnittlichen Anfrage zum Datensatz 
                    entsprechen soll. Zur Sicherheit mache ich sie noch etwas
                    länger denn man weiß ja nie. Außerdem kommen ja noch die 
                    Dictionarys als String dazu. Deswegen kann es ruhig noch 
                    etwas länger sein."""
    combined_input = f"{query}\n\nData:\n{df_string}"

    encoding = tiktoken.encoding_for_model(model)

    tokens = encoding.encode(combined_input)
    st.session_state.num_tokens = len(tokens)

    MAX_TOKENS = 8192  
    st.session_state.token_usage_percent = int((st.session_state.num_tokens / MAX_TOKENS) * 100)

    
