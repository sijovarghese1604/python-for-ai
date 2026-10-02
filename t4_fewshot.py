from prompt_lab import ask

system = "Classify the sentiment of an employee's message about the new trading policy."
message = "Honestly the new 30-day holding rule is a pain, but I get why it exists."

print("=== ZERO-SHOT ===")
print(ask(message, system=system))

examples = [
    {"role": "user", "content": "Love how fast approvals are now!"},
    {"role": "assistant", "content": "POSITIVE"},
    {"role": "user", "content": "This blackout rule makes no sense, total waste of time."},
    {"role": "assistant", "content": "NEGATIVE"},
    {"role": "user", "content": "The form is okay, though a bit long."},
    {"role": "assistant", "content": "MIXED"},
]

print("\n=== FEW-SHOT ===")
print(ask(message, system=system, examples=examples))