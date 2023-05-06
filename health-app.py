import openai
import streamlit as st
from streamlit_chat import message
import os

# conversation dataset https://github.com/thu-coai/Emotional-Support-Conversation
# depression chatbot https://www.kaggle.com/datasets/nupurgopali/depression-data-for-chatbot

openai.api_key = os.getenv('OPENAI_API_KEY')

prompt = "I am a mental health assistant. I ask you questions based on your problems \
         that will lead us to understanding the real root of the problem."

def generate_response(prompt, conversation_history):
    # Combine prompt and conversation history
    prompt_with_history = f"{prompt}\n\n" + "\n\n".join(conversation_history[-20:])

    # Generate response from OpenAI API
    completion = openai.Completion.create(
        engine='text-davinci-002',
        prompt=prompt_with_history,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.4,
    )
    message = completion.choices[0].text.strip()
    return message

st.title("Healthcare App")

st.sidebar.write("Press to get your mental state")
if st.sidebar.button('Evaluate'):
    st.sidebar.write("Below you will see your evaluation evaluation...")
    # output = generate_response(prompt, st.session_state['history'])
    # st.sidebar.write(output)

# Storing the chat
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'history' not in st.session_state:
    st.session_state['history'] = []

user_input = st.text_input("You:", key='input_text_by_user')

if user_input:
    output = generate_response(prompt, st.session_state['history'] + [f"User: {user_input}"])
    st.session_state['past'].append(user_input)
    st.session_state['generated'].append(output)
    st.session_state['history'].append(f"User: {user_input}")
    st.session_state['history'].append(f"AI: {output}")

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
