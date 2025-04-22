from app.llm.generator import generate_llm_output

def generate_answer(query: str, retrieved_chunks: list) -> str:
    context = "\n".join(retrieved_chunks)
    return generate_llm_output(query, context)
