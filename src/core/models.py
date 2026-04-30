from pydantic import BaseModel, Field
from typing import List

class TestCase(BaseModel):
    title: str = Field(description="Short, descriptive title of the test")
    steps: List[str] = Field(description="Step-by-step instructions")
    expected_result: str = Field(description="What the successful outcome looks like")
    priority: str = Field(description="High, Medium, or Low")
    test_type: str = Field(description="Functional, Edge Case, or Security")

class RequirementAnalysis(BaseModel):
    gherkin_feature: str = Field(description="The full Gherkin .feature file content")
    test_cases: List[TestCase] = Field(description="List of structured test cases")
    coverage_score: int = Field(description="Estimated coverage percentage (0-100)")
