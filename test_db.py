# test_database.py

from src.database import Database
import numpy as np
import json

print("\n🔍 Testing Database Logging with NumPy data types...\n")

# Initialize database
db = Database()

# Fake test data (similar to your real chatbot chunks)
fake_chunks = [
    {"document": "test.pdf", "page": 1, "chunk_id": 0, "score": np.float32(0.875)},
    {"document": "test.pdf", "page": 2, "chunk_id": 1, "score": np.float64(0.752)}
]

fake_answer = "TechVision Solutions’ mission is to drive digital innovation."

# Try to log an interaction
try:
    interaction_id = db.log_interaction(
        question="What is TechVision Solutions' mission?",
        chunks=fake_chunks,
        answer=fake_answer,
        citations=fake_chunks,
        execution_time=0.45
    )

    print(f"✅ Logged interaction successfully with ID: {interaction_id}")
except Exception as e:
    print(f"❌ Error while logging interaction: {e}")

# Retrieve logs to confirm entry
logs = db.get_chat_logs(limit=3)
print("\n🧾 Recent chat logs:")
for row in logs:
    print(row)
