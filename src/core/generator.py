import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from src.core.models import RequirementAnalysis

load_dotenv()

class TestGenerator:
    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        
        self.llm = ChatAnthropic(
            # Using Haiku to bypass the 404 access issue
            model="claude-sonnet-4-6", 
            temperature=0,
            api_key=api_key
        ).with_structured_output(RequirementAnalysis)

    def generate_from_text(self, requirement_text: str):
        prompt = f"""
        You are a Senior Staff Software Test Engineer. 
        Analyze the following requirement and generate:
        1. Professional Gherkin .feature file.
        2. Detailed test cases (including happy path and edge cases).
        3. A coverage assessment.

        Requirement:
        {requirement_text}
        """
        return self.llm.invoke(prompt)
