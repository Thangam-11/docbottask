# src/llm_engine.py

import os
from dotenv import load_dotenv
from groq import Groq
from logger import get_logger


class LLMEngine:
    """LLM Engine using Groq API with Llama 3.1"""

    def __init__(self):
        load_dotenv()
        self.logger = get_logger(__name__)
        self.api_key = os.getenv("GROQ_API_KEY")
        self.model = os.getenv("LLM_MODEL", "llama-3.1-8b-instant")

        if not self.api_key:
            raise ValueError("❌ GROQ_API_KEY not found in .env file!")

        # Initialize Groq client
        try:
            self.client = Groq(api_key=self.api_key)
            self._verify_model()
            self.logger.info(f"✅ LLM Engine initialized successfully with model: {self.model}")
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize Groq LLM: {e}")
            raise

    def _verify_model(self):
        """Ping the model with a small prompt to verify connectivity"""
        try:
            self.logger.info(f"🔍 Verifying connection with model '{self.model}'...")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": "ping"}],
                max_tokens=1
            )
            if response and response.choices:
                self.logger.info(f"✅ Model '{self.model}' is active and responding.")
            else:
                self.logger.warning(f"⚠️ Model '{self.model}' returned an empty response.")
        except Exception as e:
            self.logger.error(f"❌ Model verification failed: {e}")
            raise

    def generate(self, prompt):
        """Generate response from the LLM model"""
        try:
            self.logger.info(f"🧠 Generating response using model: {self.model}")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=512,
            )

            # ✅ FIX: Access message content properly
            answer = response.choices[0].message.content.strip()

            self.logger.info("✅ Response generated successfully.")
            return answer

        except Exception as e:
            self.logger.error(f"❌ Error generating response: {e}")
            return f"[Error] {e}"

