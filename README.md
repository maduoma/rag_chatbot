# RAG Chatbot

A production-grade Retrieval-Augmented Generation (RAG) chatbot system with a FastAPI backend, Flask UI, and FAISS vectorstore. Designed for document Q&A with modern, user-friendly features.

---

## 🚀 Features

- **Document Upload & Ingestion**: Supports PDF, TXT, DOCX, CSV
- **Chunking & Embedding**: Sentence Transformers for semantic search
- **Vector Search**: FAISS for fast retrieval
- **LLM-powered Chat**: Integrates with OpenAI API (or local LLM)
- **REST API**: Built with FastAPI
- **Modern Web UI**: Flask-based, with:
  - Multi-session support with session titles
  - Collapsible & deletable sidebar sessions
  - Distinct user/assistant chat bubbles with avatars (👤/🤖)
  - Markdown & LaTeX rendering (marked.js + MathJax)
  - Dark mode toggle 🌙/☀️
  - Edit & resend previous queries (✏️)
  - Copy assistant responses (📋)
  - Responsive, polished design
- **Testing**: Pytest-based test suite
- **Dockerized**: For easy deployment

---

## 🏗️ Architecture & Folder Structure

```
rag_chatbot/
├── app/
│   ├── api/           # FastAPI backend (routes, main, logic)
│   ├── llm/           # LLM integration and generators
│   ├── ui/            # Flask UI (routes.py, templates/)
│   │   └── templates/ # HTML templates (index.html, layout.html)
│   ├── vectorstore/   # FAISS index and vector DB logic
│   ├── ingestion.py   # Document processing and chunking
│   └── utils/         # Helper functions (helpers.py)
├── tests/             # Pytest test suite
├── requirements.txt   # Python dependencies
├── Makefile           # Common commands
├── .env.example       # Environment variable template
└── README.md
```

- **processed/**: For storing pre-processed/chunked docs (created at runtime)
- **faiss/**: For FAISS index files (created at runtime)

---

## ⚡ Quickstart

### 1. Install dependencies
```sh
make install
# or
pip install -r requirements.txt
```

### 2. Set up environment variables
Copy `.env.example` to `.env` and set:
```
OPENAI_API_KEY=your-key-here
API_URL=http://localhost:8000
SECRET_KEY=your-flask-secret
```

### 3. Start the backend (FastAPI)
```sh
uvicorn app.api.main:app --reload
```

### 4. Start the UI (Flask)
```sh
export FLASK_APP=app.ui.flask_app
flask run
# or use the Makefile: make ui
```

### 5. (Optional) Run with Docker
```sh
docker-compose up --build
```

---

## 🧪 Testing
Run all tests:
```sh
pytest tests/
```

---

## 💻 Usage & UI Guide

- **Upload Documents**: Use the sidebar or upload page to add PDFs, DOCX, CSV, or TXT files.
- **Multi-Session Chat**: Start new chats, switch sessions, and see chat titles in the sidebar.
- **Sidebar Management**: Collapse sidebar, delete sessions (⋯ → 🗑️), and create new chats.
- **Chat Experience**:
  - User queries and assistant responses are shown in visually distinct bubbles with avatars.
  - **Markdown & LaTeX**: Assistant answers support markdown (bold, lists, code) and LaTeX math.
  - **Dark Mode**: Toggle 🌙/☀️ for dark/light themes.
  - **Edit & Resend**: Click ✏️ on a user message to edit and resend.
  - **Copy Response**: Click 📋 on an assistant message to copy to clipboard.

---

## 🛠️ Production Notes
- Use a production WSGI server (e.g., Gunicorn) for Flask in production
- Set strong secrets and API keys in `.env`
- Secure file uploads and validate input
- Monitor logs and errors

---

## ❓ FAQ / Troubleshooting
- **OpenAI API Key not recognized?**
  - Ensure `.env` is in the project root and loaded by both Flask and FastAPI.
- **UI not updating?**
  - Clear browser cache or restart Flask server after changes.
- **Vectorstore errors?**
  - Check FAISS and sentence-transformers are installed and compatible.
- **Test failures?**
  - Ensure all dependencies are installed and environment variables are set for test mode.

---

## 📂 Folder Descriptions
- **processed/**: Stores processed/chunked docs for retrieval (created at runtime)
- **faiss/**: Stores FAISS vector indexes (created at runtime)
- **utils/**: Helper functions used across modules

---

## License
MIT


### 2. Run locally
```sh
make run-api
make run-ui
```

### 3. Run tests
```sh
make test
```

### 4. Build and run with Docker Compose
```sh
docker compose -f docker/docker-compose.yml up --build
```

## Configuration
- Environment variables: see `docker/.env`
- Data storage: `data/` directory

## Project Structure
```
(app structure as provided)
```

## Production Notes
- Use a production WSGI server (e.g., Gunicorn) for Flask in production
- Set strong secrets and API keys in `.env`
- Secure file uploads and validate input
- Monitor logs and errors

## License
MIT
