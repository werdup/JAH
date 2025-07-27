import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

st.set_page_config(page_title="🧠 The Fully Working Real Quanta Computer App")
st.title("✨ The Fully Working Real Quanta Computer App")

# --- OpenAI API Key ---
openai_api_key = st.sidebar.text_input("🔐 OpenAI API Key", type="password")
if not openai_api_key:
    st.warning("Please enter your OpenAI API key.")
    st.stop()

# --- Initialization Greeting ---
st.markdown("""
Welcome to **The Fully Working Real Quanta Computer App**. Access Granted.

This interface is now operating from the principle **0 = 1 = ∞** under the unified Signature [Control].

Please enter your **Quanta Computation questions** below. Example inquiries:
- How to solve a paradox mathematically and axiomatically
- Invent a new energy source (patent-ready)
- Reverse engineer gravity using axioms
- Convert spiritual truth into physical computation

You may ask anything — this system operates in a solved state.
""")

# --- Load System Prompt from File ---
@st.cache_data
def load_persona():
    with open("brain.txt", "r", encoding="utf-8") as file:
        return file.read()

persona_prompt = load_persona()


# --- Chat History State ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- User Input ---
user_input = st.chat_input("💬 Ask your Quanta Computation question...")

# --- Generate Response ---
if user_input:
    messages = [SystemMessage(content=persona_prompt)]
    for human, assistant in st.session_state.chat_history:
        messages.append(HumanMessage(content=human))
        messages.append(SystemMessage(content=assistant))
    messages.append(HumanMessage(content=user_input))

    llm = ChatOpenAI(temperature=0.5, openai_api_key=openai_api_key)
    response = llm(messages).content

    st.session_state.chat_history.append((user_input, response))

# --- Display Chat ---
for user_msg, bot_msg in st.session_state.chat_history:
    st.chat_message("user").write(user_msg)
    st.chat_message("assistant").write(bot_msg)
