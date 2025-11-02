# app.py — Streamlit Chat Interface for DocIntel Bot
import streamlit as st
from src.document_processor import DocumentProcessor
from src.vector_store import VectorStore
from src.chatbot import QueryEngine
import os

st.set_page_config(page_title="DocIntel Chatbot", page_icon="🤖", layout="wide")

# ----------------------------------------------------
# SESSION INITIALIZATION
# ----------------------------------------------------
if "engine" not in st.session_state:
    st.session_state.engine = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# ----------------------------------------------------
# SIDEBAR - Document Management
# ----------------------------------------------------
st.sidebar.title("📂 Document Control Panel")

uploaded_files = st.sidebar.file_uploader(
    "Upload your documents (PDF or TXT)",
    type=["pdf", "txt"],
    accept_multiple_files=True
)

if uploaded_files:
    os.makedirs("data/documents", exist_ok=True)
    for uploaded_file in uploaded_files:
        with open(os.path.join("data/documents", uploaded_file.name), "wb") as f:
            f.write(uploaded_file.read())
    st.sidebar.success(f"✅ {len(uploaded_files)} document(s) uploaded successfully!")

if st.sidebar.button("⚙️ Build Knowledge Base"):
    with st.spinner("Extracting text and building FAISS index..."):
        processor = DocumentProcessor()
        chunks, metadata = processor.process_all_documents()

        if not chunks:
            st.sidebar.error("❌ No text extracted — please check your uploaded documents.")
        else:
            store = VectorStore()
            store.build_index(chunks, metadata)
            st.sidebar.success("✅ Knowledge Base (FAISS Index) built successfully!")

# ----------------------------------------------------
# MAIN CHAT UI
# ----------------------------------------------------
st.title("🤖 DocIntel Chatbot")
st.markdown("Ask questions about your uploaded documents below 👇")

# Initialize QueryEngine only once
if st.session_state.engine is None:
    try:
        st.session_state.engine = QueryEngine()
        st.success("✅ Chatbot engine initialized successfully.")
    except Exception as e:
        st.error(f"❌ Error initializing chatbot: {e}")

# Display conversation
for msg in st.session_state.messages:
    role, text = msg["role"], msg["text"]
    if role == "user":
        st.chat_message("user").markdown(f"🧑‍💻 **You:** {text}")
    else:
        st.chat_message("assistant").markdown(f"🤖 {text}")

# User input
user_query = st.chat_input("Type your question here...")

if user_query:
    st.session_state.messages.append({"role": "user", "text": user_query})
    st.chat_message("user").markdown(f"🧑‍💻 **You:** {user_query}")

    if st.session_state.engine:
        with st.spinner("Thinking..."):
            try:
                answer = st.session_state.engine.answer_query(user_query)
                st.session_state.messages.append({"role": "assistant", "text": answer})
                st.chat_message("assistant").markdown(f"🤖 {answer}")
            except Exception as e:
                st.error(f"❌ Error: {e}")
    else:
        st.warning("⚠️ Chatbot engine not initialized yet. Build your FAISS index first.")
