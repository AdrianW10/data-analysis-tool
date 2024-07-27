import streamlit as st
import sys
import re
import time
from io import StringIO

# Class to convert the thought process into a string, which is redirected from 
# stdout to be displayed by Streamlit.
# The method display_text(self) ensures that the thought process is nicely 
# formatted for output.
class CapturingThoughtProcess(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # Free up memory
        sys.stdout = self._stdout

    def display_text(self):
        # Save the captured text as a string
        text = " ".join(self)
        # Filter only the relevant sections from the thought process
        thought = re.search(r"Thought: (.*?)Action:", text)
        action = re.search(r"Action:.*1;3m(.*?)Final Answer:", text)
        #answer = re.search(r"Final Answer: (.*?)\x1b", text)
        # Output through Streamlit
        try:
            st.write(f"{thought.group(1)}\n\n")
            time.sleep(0.5)
            st.write(f"{action.group(1)}\n\n")
            #time.sleep(0.5)
            #st.success(f"{answer.group(1)}")
        except:
            st.warning("Could not extract the thought process.")
