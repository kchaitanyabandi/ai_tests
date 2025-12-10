# ai_tests

## Setup (uv + venv)

- **Prereqs:** macOS with Homebrew.

- **Install uv:**
	- zsh
		brew install uv

- **Create a virtual env (managed by uv):**
	- zsh
		cd /Users/kcbandi/Downloads/ai_tests
		uv venv .venv

- **Activate the env:**
	- zsh
		source .venv/bin/activate

- **Install dependencies:**
	- zsh
		uv pip install -e .

- **Set your OpenAI key (required by scripts):**
	- zsh
		export OPENAI_API_KEY="sk-..."
		echo 'export OPENAI_API_KEY="sk-..."' >> ~/.zshrc

- **Run examples:**
	- zsh
		python edit_with_predicted_outputs.py

- **Deactivate env (optional):**
	- zsh
		deactivate

## Notes

- `.env` files are ignored by git; use `.env.example` as a template.
- If you use VS Code, select the interpreter at `.venv/bin/python`.
