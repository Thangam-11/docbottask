"""
Chatbot Query Engine — integrates FAISS retrieval + Groq LLM response generation
"""

import numpy as np
from src.vector_store import VectorStore
from src.llm_engine import LLMEngine
from src.database import Database
from logger import get_logger


class QueryEngine:
    def __init__(self):
        self.logger = get_logger(__name__)
        self.store = VectorStore()
        self.llm = LLMEngine()
        self.db = Database()
        self.index, self.metadata = self.store.load_index()
        self.logger.info("✅ QueryEngine initialized successfully.")

    # ---------------------------------------------------
    # 1️⃣ Retrieve relevant chunks from FAISS
    # ---------------------------------------------------
    def retrieve_relevant_chunks(self, query, top_k=3):
        query_emb = self.store.generate_embeddings([query])
        distances, indices = self.index.search(query_emb, top_k)

        results = []
        for i, idx in enumerate(indices[0]):
            result = self.metadata[idx]
            result["score"] = 1.0 / (1.0 + distances[0][i])
            results.append(result)

        self.logger.info(f"🔍 Retrieved top {top_k} chunks for query.")
        return results

    # ---------------------------------------------------
    # 2️⃣ Generate an answer using Groq LLM
    # ---------------------------------------------------
    def generate_answer(self, query, context_chunks):
        context_text = "\n".join([chunk["text"] for chunk in context_chunks])
        prompt = f"""
        You are an AI assistant answering questions based on document content.
        Context:
        {context_text}
        
        Question: {query}
        Answer:
        """

        answer = self.llm.generate(prompt)
        return answer

    # ---------------------------------------------------
    # 3️⃣ Full pipeline: retrieve + reason + store
    # ---------------------------------------------------
    def answer_query(self, query):
        self.logger.info(f"🤖 Received query: {query}")
        retrieved = self.retrieve_relevant_chunks(query)
        answer = self.generate_answer(query, retrieved)

        # Log the interaction in DB
        self.db.log_interaction(query, retrieved, answer, citations=retrieved)

        print("\n🧠 Answer:\n", answer)
        return answer


# ---------------------------------------------------
# 🧪 Test it standalone
# ---------------------------------------------------
if __name__ == "__main__":
    engine = QueryEngine()
    test_query = "What is TechVision Solutions' mission?"
    engine.answer_query(test_query)
