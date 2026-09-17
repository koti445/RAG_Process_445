from openai import OpenAI

from src.core.config import get_settings


class Generator:
    SYSTEM_PROMPT = """You are a helpful assistant.
Answer ONLY using the provided context.
If the answer is not in the context, say: "I don't have enough information to answer."
Mention which chunk(s) you used when possible."""

    def __init__(self) -> None:
        settings = get_settings()
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.llm_model

    def generate(self, question: str, context_chunks: list[str]) -> str:
        if not context_chunks:
            return "I don't have enough information to answer."

        context = "\n\n---\n\n".join(
            f"[Chunk {index + 1}]\n{chunk}" for index, chunk in enumerate(context_chunks)
        )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": f"Context:\n{context}\n\nQuestion: {question}",
                },
            ],
            temperature=0.2,
        )

        return response.choices[0].message.content or ""