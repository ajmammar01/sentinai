from openai import OpenAI
from ..domain.entities import ProcessingResponse
from ..infrastructure.llm_client import LLMClient

class EmailProcessor:
    def __init__(self):
        self.llm_client = LLMClient()
        self.client = self.llm_client.get_client()
        self.model = self.llm_client.model

    def process_email(self, email_content: str) -> ProcessingResponse:
        """
        Takes raw email text and converts it into a validated Pydantic object
        using OpenAI's Structured Outputs.
        """
        
        system_prompt = (
            "You are an expert support triage assistant. "
            "Analyze the email and extract structured data. "
            "If the content is spam, offensive, or gibberish, use the 'flagged' type."
        )

        # This is the magic part: 'response_format' forces the LLM to follow your Pydantic model
        completion = self.client.beta.chat.completions.parse(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Process this email content:\n\n{email_content}"}
            ],
            response_format=ProcessingResponse,
        )

        # This returns a fully validated 'ProcessingResponse' object
        return completion.choices[0].message.parsed