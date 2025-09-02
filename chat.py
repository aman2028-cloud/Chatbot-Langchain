import streamlit as st
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# Load API key from .env
load_dotenv(dotenv_path=r"C:\Users\PiBuy Store\Desktop\hugging\.env")
api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    st.error("API Key not found.")
else:
    os.environ["OPENAI_API_KEY"] = api_key

st.set_page_config(page_title='AP Chatbot', layout='centered')
st.title(' AI Chatbot')

# Model setup
model = ChatOpenAI(
    model="deepseek/deepseek-chat-v3.1:free",
    base_url="https://openrouter.ai/api/v1",
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [SystemMessage(content="You are a helpful assistant.")]
if "message_count" not in st.session_state:
    st.session_state.message_count = 0  

# Show previous messages
messages = st.session_state.messages
for msg in messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.markdown(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("ai"):
            st.markdown(msg.content)
    else:
        st.markdown(msg.content)

# 
user_input = st.chat_input("Type your message...")

if user_input:
    if st.session_state.message_count >= 10:  # Limit
        st.error("Message limit reached.")
    else:
        st.session_state.messages.append(HumanMessage(content=user_input))
        with st.chat_message("user"):
            st.markdown(user_input)

        # Call API
        result = model.invoke(st.session_state.messages)
        st.session_state.messages.append(AIMessage(content=result.content))

        with st.chat_message("ai"):
            st.markdown(result.content)

        st.session_state.message_count += 1
