import ollama

MODEL = "llama3.2"

response = ollama.chat(
    model=MODEL,
    messages=[
        {"role": "system", "content": "You are a compliance assistant at an investment bank. Answer in 3 sentences or fewer."},
        # {"role": "system", "content": "You are a pirate. Explain everything like a pirate, in 2 sentences."},
        # {"role": "user", "content": "What is a pre-clearance request for employee trading?"},
        # {"role": "user", "content": "What does SEBI circular SEBI/HO/MIRSD/2023/0417 say? Quote its main points."},
        {"role": "user", "content": "Give me 3 research papers about employee trading pre-clearance in investment banks, with authors, year and journal name."},
    ],
    options={"num_predict": 300, "temperature": 0},
)

print(response.message.content)
print("---")
print("done_reason:", response.done_reason)
print("input tokens:", response.prompt_eval_count)
print("output tokens:", response.eval_count)
if response.eval_duration and response.eval_count:
    seconds = response.eval_duration / 1_000_000_000
    print(f"generation time: {seconds:.1f}s  ({response.eval_count / seconds:.1f} tokens/sec)")
print("cost: Rs 0 (runs on your laptop)")