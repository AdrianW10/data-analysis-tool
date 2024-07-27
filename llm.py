import streamlit as st
from openai import OpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import tiktoken
import re
from thought_process import CapturingThoughtProcess

# Client must be defined here again
load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
chat = ChatOpenAI(model_name="gpt-4", temperature=0.0)

pre_promt = """Besides giving a verbal overview 
                of the data, please also think about a few (maximum 5)
                sample questions for the data that one could ask an AI to find 
                out more about the data. Put them in the end of your answer
                with an header that says 'Exemplary questions:' \n\n"""

pre_promt_no_sum = """Please think about a few (maximum 5)
                sample questions for the data that one could ask an AI to find 
                out more about the data. Put them in your answer
                with an header that says 'Exemplary questions:' \n\n"""

def use_chatGPT(query, option_summary):
    template = {
                "role": "system", "content": """You are a helpful model that 
                answers questions about a CSV file based on the provided data 
                information. """, 
                
                "role": "user", "content": f"{pre_promt}" if option_summary 
                                                    else f"{pre_promt_no_sum}"
                }

    template["content"] += query
    
    response = client.chat.completions.create(
        messages=[template],
        model="gpt-4",
        stream=option_summary,
            )
    return response

def chatbot(option_answer, option_plot, chat_history):
    # Display chat history (if any)
    for message in chat_history:
        with st.chat_message(message["role"]):
            if re.search(r"import", message["content"]):
                try: exec(message["content"]) 
                except: pass
            else:
                st.markdown(message["content"])
    
    if prompt := st.chat_input("Send a question"):
        chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
    
    if option_answer and option_plot:
        st.warning("Thought process cannot be displayed along with graphics.")
    
    if prompt is None and len(chat_history) == 0:
        with st.chat_message("assistant"):
            st.write("What would you like to know about the data?\n\n" + 
                                        st.session_state.exemplary_questions)
    elif prompt is None:
        with st.chat_message("assistant"):
            st.write("What would you like to know about the data?")

    else:
        with st.spinner("Analyzing data..."):
            with st.chat_message("assistant"):
                response = response_manager(option_answer, option_plot, prompt)
                if not option_plot: 
                    st.write(response)
                chat_history.append({"role": "assistant", "content": response})

def response_manager(option_answer, option_plot, prompt):
    if not option_answer and not option_plot:
        response = analyse_csv_data(prompt)
    elif option_answer and not option_plot:
        with CapturingThoughtProcess() as output:
            response = analyse_csv_data(prompt)
        output.display_text()
    elif option_plot:
        prompt += """\nPlease provide only the code that generates the graphic 
        as a response. Replace 'df' with 'st.session_state.df' and 'plt.show()' 
        with 'st.pyplot(plt, clear_figure=True)' and set the plot's figsize 
        to (10,5)."""
        
        code = analyse_csv_data(prompt)
        fixed_code = re.search(r"```python(.*)```", code, re.DOTALL)
        try: response = fixed_code.group(1); exec(fixed_code.group(1))
        except: st.error("Something went wrong, please try again.")
    return response

def analyse_csv_data(query):
    agent = create_pandas_dataframe_agent(chat, 
        st.session_state.df if st.session_state.df_filtered is None 
        else st.session_state.df_filtered, 
        verbose=True
        ) 
    response = agent.run(query)
    
    return response

def calc_token_usage(model="gpt-4"):
    df_string = st.session_state.df.head(6).to_string(index=False)
    query = """This is an example query that should roughly correspond to the 
    average token count of a typical dataset query. 
    To be safe, I'll make it a bit longer"""
    combined_input = f"{query}\n\nData:\n{df_string}"

    encoding = tiktoken.encoding_for_model(model)

    tokens = encoding.encode(combined_input)
    st.session_state.num_tokens = len(tokens)

    MAX_TOKENS = 8192  
    st.session_state.token_usage_percent = int(
                            (st.session_state.num_tokens / MAX_TOKENS) * 100)
