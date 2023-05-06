import openai
import streamlit as st
from streamlit_chat import message
import os

# conversation dataset https://github.com/thu-coai/Emotional-Support-Conversation
# depression chatbot https://www.kaggle.com/datasets/nupurgopali/depression-data-for-chatbot

openai.api_key = os.getenv('OPENAI_API_KEY')

prompt0 = "You are a mental health assistant. I ask you questions based on problems \
         that will lead us to understanding the real root of the problem."

def generate_response():
    messages = [{'role': 'assistant' if message.startswith("AI:") else 'user', 'content':message[3:] if message.startswith("AI:") else message} for message in st.session_state['history']]
    completion = openai.ChatCompletion.create(model = "gpt-4",messages =  messages )
    message = completion["choices"][0]["message"]['content']
    return message

st.title("Healthcare App")


# Storing the chat
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'history' not in st.session_state:
    st.session_state['history'] = [prompt0]

user_input = st.text_input("You:", key='input_text_by_user')

st.sidebar.write("Press to get your mental state")
if st.sidebar.button('Evaluate'):
    st.sidebar.write("Below you will see your evaluation evaluation...")
    st.session_state['history'].append(f"Patient: Based on our \
        chat history give me an evaluation of my mental health state.")
    output = generate_response()
    st.session_state['history'] = st.session_state['history'][:-1]
    st.sidebar.write(output)
else:
    if user_input:
        st.session_state['history'].append(user_input)
        output = generate_response()
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(output)
        st.session_state['history'].append(f"AI:{output}")

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
