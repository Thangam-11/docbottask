# 🤖 DocIntel Bot

> **A local document intelligence and question-answering system powered by FAISS, Groq LLM, and Streamlit**

DocIntel Bot is an intelligent document assistant that enables users to upload documents (PDFs and text files), build a knowledge base, and interact with the content through natural language queries.  
It uses **FAISS** for efficient vector search, **Hugging Face embeddings** for semantic representation, and **Groq's Llama 3.1** for intelligent response generation — all wrapped in a clean **Streamlit web app**.

---

## ✨ Features

- **📄 Multi-format Document Support** — Upload and process PDF or TXT files effortlessly.
- **🔍 Semantic Search with FAISS** — Retrieve relevant chunks using powerful vector embeddings.
- **🧠 AI-Powered LLM Responses** — Uses Groq's Llama 3.1 model for context-aware answers.
- **💬 Interactive Chat Interface** — Streamlit-powered chat UI with memory and retrieval.
- **📊 Smart Database Logging** — Logs all queries, answers, and citations in SQLite.
- **🔧 Configurable Architecture** — Easily change paths and models from YAML config.
- **📝 UTF-8 Safe Logging System** — Clean, colorful, and robust error tracking.

---

## 🧱 Architecture Overview

```
DocIntel Bot
├── Document Processor → PDF/TXT extraction & chunking
├── Vector Store (FAISS) → Semantic embedding & indexing
├── Query Engine → Retrieval-Augmented Generation (RAG)
├── LLM Engine (Groq) → Natural Language Generation
└── Database → Logging, analytics, and test results
```

---

## 🧩 Prerequisites

Before running, ensure you have:

- 🐍 Python **3.8+**
- 🔑 **Groq API Key** — [Get one here](https://console.groq.com)
- 🤗 **Hugging Face Token** — [Get one here](https://huggingface.co/settings/tokens)

---

## ⚙️ Installation

### 1️⃣ Clone Repository
```bash
git clone https://github.com/yourusername/docintel-bot.git
cd docintel-bot
```

### 2️⃣ Create Virtual Environment
```bash
python -m venv botdocvenv
botdocvenv\Scripts\activate  # On Windows
# or
source botdocvenv/bin/activate  # On macOS/Linux
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables
Create a `.env` file in your project root:

```env
GROQ_API_KEY=your_groq_api_key_here
LLM_MODEL=llama-3.1-8b-instant
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token_here
EMBEDDING_MODEL=BAAI/bge-small-en-v1.5
```

---

## 🚀 Usage

### 🧠 Option 1: Streamlit Web Interface (Recommended)
```bash
streamlit run app.py
```

Then open your browser at:
```
http://localhost:8501
```

**➡️ Features in the UI:**
- Upload PDFs or text files
- Click "⚙️ Build Knowledge Base" to create FAISS index
- Start chatting naturally with your documents

### 🧱 Option 2: Command-Line Index Builder
```bash
python build_index.py
```

### 🧪 Option 3: Programmatic Access
```python
from src.chatbot import QueryEngine

engine = QueryEngine()
answer = engine.answer_query("What is TechVision Solutions' mission?")
print(answer)
```

---

## 📁 Project Structure

```bash
docintel-bot/
│
├── app.py                      # Streamlit web interface
├── build_index.py              # CLI index builder
├── .env                        # Environment variables
├── .gitignore
├── README.md
├── requirements.txt
│
├── src/
│   ├── document_processor.py   # PDF/Text extraction
│   ├── vector_store.py         # FAISS-based vector index
│   ├── llm_engine.py           # Groq API integration
│   ├── chatbot.py              # Query engine (RAG)
│   ├── database.py             # SQLite logging
│   └── logger/                 # Config + logging system
│
├── data/
│   ├── documents/              # Upload PDFs/TXTs here
│   ├── faiss_index.bin         # Generated FAISS index
│   ├── chunks_metadata.pkl     # Chunk metadata
│   └── docintel.db             # SQLite database
│
├── models/
│   ├── embedding_model/        # Hugging Face model
│   └── tinyllama/              # Local LLM model
│
└── logs/
    └── docintel.log
```

---

## 🧮 Database Schema

### `chat_logs`
| id | timestamp | question | answer | citations | execution_time |
|----|-----------|----------|--------|-----------|----------------|

### `test_queries`
| id | query | expected_topic | answer | success | timestamp |
|----|-------|----------------|--------|---------|-----------|

### `system_metrics`
| id | metric_name | metric_value | metadata | timestamp |
|----|-------------|--------------|----------|-----------|

---

## 🧰 Configuration (Optional)

**File:** `configure/config.yaml`

```yaml
models:
  embedding: "models/embedding_model"
  llm: "models/tinyllama"

paths:
  database: "data/docintel.db"
  documents: "data/documents"
  faiss_index: "data/faiss_index.bin"
  metadata: "data/chunks_metadata.pkl"

chunking:
  chunk_size: 500
  chunk_overlap: 50

retrieval:
  top_k: 3
```

---

## 🧠 Testing

### 🧾 Test Database
```bash
python test_db.py
```

### 📄 Test Document Processor
```bash
python -m src.document_processor
```

### 🔍 Test FAISS Retrieval
```bash
python -m src.vector_store
```

### 🧠 Example Query

**User:** *What is TechVision Solutions' mission?*

**Bot:** *TechVision Solutions' mission is to empower organizations with cutting-edge tools and expert guidance to achieve sustainable growth and competitive advantage in the digital age.*

---

## 🛠️ Troubleshooting

| Problem | Solution |
|---------|----------|
| ❌ FAISS index not found | Run `python build_index.py` or click "Build Knowledge Base" |
| 🧱 Invalid API Key | Check `.env` and verify your Groq/Hugging Face keys |
| ⚠️ No text extracted | Ensure your PDFs are text-based (not scanned images) |
| 💾 DB write errors | Delete `data/docintel.db` and retry |
| 🔡 UnicodeEncodeError | Run Python 3.8+ (UTF-8 is default) |

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [FAISS](https://github.com/facebookresearch/faiss)
- [Groq](https://groq.com)
- [Sentence Transformers](https://www.sbert.net/)
- [Streamlit](https://streamlit.io)

---

## 🗺️ Roadmap

- [ ] Add support for DOCX & Markdown files
- [ ] Multi-language embeddings
- [ ] User authentication for enterprise mode
- [ ] OCR support for scanned PDFs
- [ ] Docker containerization
- [ ] REST API endpoints

---

## 💬 Contact

👨‍💻 **Thangarasu**  
📧 Email: thangamani1128@gmail.com  
🌐 Project: [GitHub Repo](https://github.com/yourusername/docintel-bot)

---

<div align="center">

**Made with ❤️ by Thangarasu**

⭐ **Star this repository if you found it useful!**

</div>

---



```
AI • Chatbot • Streamlit • FAISS • LLM • RAG • Groq • NLP • Document Intelligence
```
