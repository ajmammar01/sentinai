import os
from openai import OpenAI
from dotenv import load_dotenv

# Load `.env` reliably even when cwd != project root.
# Your project currently keeps it at `app/.env`.
_dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
load_dotenv(dotenv_path=_dotenv_path, override=False)

class LLMClient:
    def __init__(self):
        # We get the key from memory, NOT from the code
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise RuntimeError(
                "OPENAI_API_KEY not found. Ensure it's set in the environment or in app/.env."
            )
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-4o-mini" # Fast, cheap, and supports structured outputs

    def get_client(self):
        return self.client