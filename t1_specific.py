from prompt_lab import ask

vague = "Tell me about insider trading."

specific = """Explain insider trading to a new software engineer joining a bank.
- Use exactly 3 bullet points.
- Each bullet under 20 words.
- Include one simple example.
- No legal jargon."""

print("=== VAGUE ===")
print(ask(vague))
print("\n=== SPECIFIC ===")
print(ask(specific))