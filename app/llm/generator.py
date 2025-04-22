import os
import openai
from dotenv import load_dotenv

# Load .env files from both root and docker/ for flexibility
root_env = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../.env'))
docker_env = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../docker/.env'))

root_loaded = load_dotenv(dotenv_path=root_env)
docker_loaded = load_dotenv(dotenv_path=docker_env)

# Debug logging to verify environment loading (does not log secret values)
def _debug_env():
    print(f"[DEBUG] Loaded .env from root: {root_env} -> {root_loaded}")
    print(f"[DEBUG] Loaded .env from docker/: {docker_env} -> {docker_loaded}")
    print(f"[DEBUG] OPENAI_API_KEY set: {bool(os.environ.get('OPENAI_API_KEY'))}")
    print(f"[DEBUG] API_KEY set: {bool(os.environ.get('API_KEY'))}")
_debug_env()

# Set OpenAI API key
openai.api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("API_KEY")

if not openai.api_key:
    if os.environ.get("PYTEST_CURRENT_TEST"):  # allow tests to run without key
        print("[WARNING] OpenAI API key not found — using test key for CI/testing.")
        openai.api_key = "test-key"
    else:
        raise RuntimeError("OpenAI API key not found in environment variables. Please set OPENAI_API_KEY or API_KEY.")

def generate_llm_output(query: str, context: str) -> str:
    prompt = f"You are a helpful assistant. Use the following context to answer the user's question.\n\nContext:\n{context}\n\nQuestion: {query}\n\nAnswer:"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for answering questions about the provided document."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=512,
            temperature=0.2,
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"[OpenAI API error: {e}]"
