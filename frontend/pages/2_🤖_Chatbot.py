import streamlit as st
import backoff
import pandas as pd
import requests
from langchain_experimental.agents import create_csv_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from dotenv import load_dotenv
from requests.exceptions import HTTPError

load_dotenv()
# Streamlit UI setup
st.set_page_config(page_title="Chatbot", layout="centered", page_icon="🤖")



@backoff.on_exception(backoff.expo, (requests.exceptions.HTTPError, RuntimeError, ValueError), max_tries=3)
def query_gemini(agent, user_input: str):
    try:
        response = agent.invoke(user_input)
        return response
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 500:
            return "⚠️ The AI model is temporarily unavailable. Please try again later."
        else:
            return f"⚠️ Unexpected HTTP error: {e.response.status_code}"
    except Exception as e:
        return f"⚠️ Unexpected error: {str(e)}"

st.title("Chat with Your CSV 📢")
st.write("This is a general, RAG based chatbot that can answer questions about the given CSV data.\n It can covert the text query to pandas query and get the result from the CSV data.")
# Read CSV into DataFrame
# Initialize Gemini 1.5 Flash model
API_KEY = "your-google-api-key"  # Replace with your API key
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", 
                             streaming=True,
                             system_message="You are a friendly, smart and expert data analyst AI assistant. "
                            "When answering questions, always provide context, "
                            "explanations, and helpful insights rather than just numbers.")

# Create LangChain CSV Agent
agent = create_csv_agent(llm, "reddit_cleaned_v2.csv", verbose=True,allow_dangerous_code=True)

# Chat interface
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat history
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Ask a question about your CSV...")
if user_input:
    with st.chat_message("user"):
        st.write(user_input)
    with st.chat_message("assistant"):
        with st.spinner("Thinking... 🤔"):
            response = query_gemini(agent, user_input)
            st.write(response)
# User input
# user_input = st.chat_input("Ask me anything about the CSV...")
# if user_input:
#     st.session_state["messages"].append({"role": "user", "content": user_input})
#     with st.chat_message("user"):
#         st.markdown(user_input)
    
#     with st.chat_message("assistant"):
#         st_callback = StreamlitCallbackHandler(st.container())
#         response = agent.run(user_input, callbacks=[st_callback])
#         st.markdown(response)
#         st.session_state["messages"].append({"role": "assistant", "content": response})
