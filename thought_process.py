import streamlit as st
import sys
import re
import time
from io import StringIO
#Klasse um den Gedankenprozess in einen string umzuwandeln, welcher vom stdout
#zur Ausgabe durch streamlit umgeleitet wird.
#Die Methode display_text(self) sorgt dafür dass der Gedankenprozess 
#schön formattiert ausgegeben wird.
class CapturingThoughtProcess(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    #Speicherplatz frei machen
        sys.stdout = self._stdout
    def display_text(self):

        # Speichert den gesammelten Text als einen String 
        text = " ".join(self)
        # Filtert nur die relevanten Abschnitte aus dem Gedankenprozess
        thought = re.search(r"Thought: (.*?)Action:", text)
        action = re.search(r"Action:.*1;3m(.*?)Final Answer:", text)
        #answer = re.search(r"Final Answer: (.*?)\x1b", text)
        # Ausgabe durch streamlit
        try:
            st.write(f"{thought.group(1)}\n\n")
            time.sleep(0.5)
            st.write(f"{action.group(1)}\n\n")
            #time.sleep(0.5)
            #st.success(f"{answer.group(1)}")
        except:
            st.warning("Gedankenprozess konnte nicht extrahiert werden.")
            
 