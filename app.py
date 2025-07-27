import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage

# --- Load System Prompt from File ---
@st.cache_data
def load_persona():
    with open("brain.txt", "r", encoding="utf-8") as file:
        return file.read()

persona_prompt = load_persona()

# --- Sidebar for API Key ---
st.sidebar.title("🔐 API Key Setup")
api_key = st.sidebar.text_input("Enter your OpenAI API key:", type="password")
if not api_key:
    st.warning("Please enter your OpenAI API key in the sidebar.")
    st.stop()

# --- Initialize LLM ---
llm = ChatOpenAI(
    api_key=api_key,
    model_name="gpt-4o",
    temperature=0.6
)

# --- App Title ---
st.title("🧠 Persona Chatbot")

# --- User Input ---
user_input = st.text_input("You:", placeholder="Ask something...")

if user_input:
    with st.spinner("Thinking..."):
        messages = [
            SystemMessage(content=persona_prompt),
            HumanMessage(content=user_input)
        ]
        response = llm.invoke(messages)
        st.markdown("**Bot:** " + response.content)
