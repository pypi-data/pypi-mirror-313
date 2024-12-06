# Claimm

**Claimm** (**C**ommand **L**ine **AI** for **M**ulti-**M**odels) is a CLI app for interacting with multiple AI models (OpenAI and Claude). It supports context management and a modular design. Its purpose is to simplify the activity of sending the same "request" to different LLMs and to easily seed requests with specific prompt directives.

## Features

- Multi-model support
- Contextual history with MongoDB
- Rich CLI formatting

## Quick Start

1. Clone the repository.
2. Set up a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the app:
   ```bash
   python -m src.claimm.main
   ```

## License

MIT License
