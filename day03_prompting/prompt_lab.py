import ollama

MODEL = "llama3.2"
# MODEL = "qwen2.5:3b"

def ask(user: str, system: str = "", temperature: float = 0, examples: list[dict] | None = None) -> str:
    """Send one prompt to the local model and return the reply text."""
    messages: list[dict] = []
    if system:
        messages.append({"role": "system", "content": system})
    if examples:
        messages.extend(examples)          # few-shot examples go before the real question
    messages.append({"role": "user", "content": user})

    response = ollama.chat(
        model=MODEL,
        messages=messages,
        options={"temperature": temperature, "num_predict": 500},
    )
    return response.message.content or ""


if __name__ == "__main__":
    print(ask("Say hello in exactly 5 words."))