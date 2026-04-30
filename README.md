# AI Test Case Generator

A lightweight Python CLI that uses Anthropic Claude to turn a plain-language requirement into:

- A Gherkin `.feature` file
- Structured test cases
- A coverage estimate

## What it does

Given a requirement, the app analyzes it and generates:

- happy path scenarios
- edge case scenarios
- security scenarios
- a structured test case table with priority and type
- export files for downstream use

## Features

- CLI-based workflow built with `click`
- Rich terminal output with `rich`
- Structured model output with `pydantic`
- Anthropic-powered test generation using `langchain-anthropic`
- Exports generated artifacts to `data/output/`

## Project Structure

```text
src/
  main.py
  core/
    generator.py
    models.py
  utils/
```

## Requirements

- Python 3.10+
- An Anthropic API key

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root and add your Anthropic key:

```env
ANTHROPIC_API_KEY=your_api_key_here
```

## Run

From the project root:

```bash
PYTHONPATH=. python3 src/main.py
```

You will be prompted to paste a requirement.

You can also pass the requirement directly with the `--req` option:

```bash
PYTHONPATH=. python3 src/main.py --req "As a user, I want to reset my password so I can regain access to my account if I forget it."
```

## Output

The app prints the generated feature and test case table to the terminal, then exports:

- `data/output/generated_test.feature`
- `data/output/test_data.json`

## Example

Input:

```text
As a user, I want to reset my password so I can regain access to my account if I forget it.
```

Output:

- A password reset Gherkin feature
- A table of structured test cases
- A coverage score

## Notes

- The application uses `src/core/generator.py` to call Anthropic through LangChain.
- If you run the script without `PYTHONPATH=.`, Python may not resolve the `src` package correctly.
- Generated files are ignored by git via `.gitignore`.

## License

No license has been added yet. Add one before publishing the project publicly if you want to allow reuse.
