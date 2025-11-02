# build_index.py

from src.document_processor import DocumentProcessor
from src.vector_store import VectorStore

# Step 1️⃣: Extract text and create chunks
processor = DocumentProcessor()
chunks, metadata = processor.process_all_documents()

if not chunks:
    print("❌ No text extracted — check your PDF or TXT files in the 'data/documents' folder.")
    exit()

print(f"\n✅ Extracted {len(chunks)} chunks from documents.")

# Step 2️⃣: Build FAISS index
store = VectorStore()  # Model loads automatically in __init__()
store.build_index(chunks, metadata)

print("\n✅ FAISS index built and saved successfully!")
