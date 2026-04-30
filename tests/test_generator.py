import pytest
from unittest.mock import patch, MagicMock
from src.core.generator import TestGenerator
from src.core.models import RequirementAnalysis, TestCase


@pytest.fixture
def mock_anthropic():
    """Mock ChatAnthropic to avoid real API calls."""
    with patch('src.core.generator.ChatAnthropic') as mock:
        yield mock


def test_generator_returns_requirement_analysis(mock_anthropic):
    """Test that TestGenerator.generate_from_text returns a valid RequirementAnalysis."""
    
    # Create a valid RequirementAnalysis instance
    sample_test_case = TestCase(
        title="TC-01: Test Case",
        steps=["Step 1", "Step 2"],
        expected_result="Success",
        priority="High",
        test_type="Functional"
    )
    
    sample_analysis = RequirementAnalysis(
        gherkin_feature="Feature: Sample\n  Scenario: Test",
        test_cases=[sample_test_case],
        coverage_score=85
    )
    
    # Configure the mock to return our sample analysis
    mock_llm = MagicMock()
    mock_llm.invoke.return_value = sample_analysis
    mock_anthropic.return_value.with_structured_output.return_value = mock_llm
    
    # Create generator and call generate_from_text
    generator = TestGenerator()
    result = generator.generate_from_text("Test requirement text")
    
    # Assertions
    assert isinstance(result, RequirementAnalysis), "Result should be a RequirementAnalysis instance"
    assert result.gherkin_feature == "Feature: Sample\n  Scenario: Test"
    assert result.coverage_score == 85
    assert len(result.test_cases) == 1
    assert result.test_cases[0].title == "TC-01: Test Case"
    assert result.test_cases[0].priority == "High"
    assert result.test_cases[0].test_type == "Functional"


def test_generator_test_case_structure(mock_anthropic):
    """Test that generated test cases have all required fields."""
    
    test_case = TestCase(
        title="TC-02: Validation Test",
        steps=["Given something", "When action", "Then result"],
        expected_result="Expected outcome",
        priority="Medium",
        test_type="Edge Case"
    )
    
    analysis = RequirementAnalysis(
        gherkin_feature="Feature: Validation",
        test_cases=[test_case],
        coverage_score=75
    )
    
    mock_llm = MagicMock()
    mock_llm.invoke.return_value = analysis
    mock_anthropic.return_value.with_structured_output.return_value = mock_llm
    
    generator = TestGenerator()
    result = generator.generate_from_text("Validation requirement")
    
    # Verify all TestCase fields are present
    tc = result.test_cases[0]
    assert tc.title is not None
    assert isinstance(tc.steps, list)
    assert len(tc.steps) > 0
    assert tc.expected_result is not None
    assert tc.priority in ["High", "Medium", "Low"]
    assert tc.test_type in ["Functional", "Edge Case", "Security"]


def test_generator_coverage_score_range(mock_anthropic):
    """Test that coverage score is within expected range (0-100)."""
    
    for score in [0, 50, 100]:
        analysis = RequirementAnalysis(
            gherkin_feature="Feature: Test",
            test_cases=[],
            coverage_score=score
        )
        
        mock_llm = MagicMock()
        mock_llm.invoke.return_value = analysis
        mock_anthropic.return_value.with_structured_output.return_value = mock_llm
        
        generator = TestGenerator()
        result = generator.generate_from_text("Test requirement")
        
        assert 0 <= result.coverage_score <= 100, f"Coverage score {score} is out of range"


def test_generator_gherkin_output(mock_anthropic):
    """Test that generated gherkin feature is a non-empty string."""
    
    gherkin_content = """Feature: Password Reset
  Scenario: Successfully reset password
    Given user is on login page
    When user clicks "Forgot Password"
    Then user sees reset form"""
    
    analysis = RequirementAnalysis(
        gherkin_feature=gherkin_content,
        test_cases=[],
        coverage_score=90
    )
    
    mock_llm = MagicMock()
    mock_llm.invoke.return_value = analysis
    mock_anthropic.return_value.with_structured_output.return_value = mock_llm
    
    generator = TestGenerator()
    result = generator.generate_from_text("Password reset requirement")
    
    assert isinstance(result.gherkin_feature, str)
    assert len(result.gherkin_feature) > 0
    assert "Feature:" in result.gherkin_feature
