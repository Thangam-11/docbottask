from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForCausalLM
import os

# ==========================================================
# ✅ Setup local folder structure
# ==========================================================
base_dir = os.path.join(os.getcwd(), "models")
embed_dir = os.path.join(base_dir, "embedding_model")
llm_dir = os.path.join(base_dir, "tinyllama")

os.makedirs(embed_dir, exist_ok=True)
os.makedirs(llm_dir, exist_ok=True)

print(f"\n📂 Models will be saved in:\n - {embed_dir}\n - {llm_dir}")

# ==========================================================
# ✅ Download SentenceTransformer Embedding Model
# ==========================================================
print("\n🔹 Downloading SentenceTransformer model (all-MiniLM-L6-v2)...")
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
embedding_model.save(embed_dir)
print("✅ all-MiniLM-L6-v2 downloaded and saved locally!")

# ==========================================================
# ✅ Download TinyLlama Model
# ==========================================================
print("\n🔹 Downloading TinyLlama model (1.1B Chat)...")
tokenizer = AutoTokenizer.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v1.0", cache_dir=llm_dir)
model = AutoModelForCausalLM.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v1.0", cache_dir=llm_dir)
print("✅ TinyLlama model downloaded and saved locally!")

# ==========================================================
# ✅ Completion Message
# ==========================================================
print("\n🎯 All models downloaded successfully!")
print(f"📁 Embedding Model: {embed_dir}")
print(f"📁 LLM Model: {llm_dir}")
