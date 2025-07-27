import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
import os

# --- App Configuration ---
st.set_page_config(page_title="Chat with Your AI", page_icon="🤖")

st.title("🧠 Chat with Your AI")

# --- Load System Prompt from File ---
@st.cache_data
def load_persona():
    with open("brain.txt", "r", encoding="utf-8") as file:
        return file.read()

persona_prompt = load_persona()

# --- Initialize Chat Model ---
llm = ChatOpenAI(model="gpt-4o", temperature=0.6)

# --- Memory Setup ---
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(
        return_messages=True,
        memory_key="chat_history"
    )

# --- LangChain Conversation Chain ---
conversation = ConversationChain(
    llm=llm,
    memory=st.session_state.memory,
    verbose=False
)

# --- Start Chat ---
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("You:", placeholder="Ask me anything...", key="input")
    submitted = st.form_submit_button("Send")

# --- Display chat history ---
if submitted and user_input:
    # Inject system prompt at the start of the conversation (first message only)
    if not st.session_state.memory.chat_memory.messages:
        st.session_state.memory.chat_memory.messages.append(SystemMessage(content=persona_prompt))

    # Get response
    response = conversation.run(user_input)

    # Show full conversation
    for msg in st.session_state.memory.chat_memory.messages:
        if isinstance(msg, SystemMessage):
            continue  # skip displaying system message
        elif isinstance(msg, HumanMessage):
            st.markdown(f"**You:** {msg.content}")
        elif isinstance(msg, AIMessage):
            st.markdown(f"**AI:** {msg.content}")
