from prompt_lab import ask

# question = ("Give me 3 research papers about employee trading pre-clearance "
#             "in investment banks, with authors, year and journal name.")

# print("=== BEFORE (yesterday's prompt) ===")
# print(ask(question))

# safe_system = """You are a careful research assistant.
# You cannot search the internet or any database, so you cannot verify that any paper exists.
# Therefore never list paper titles, authors, years, journals or page numbers.
# For any request for papers or citations, reply exactly:
# "I can't verify specific papers. Search Google Scholar or SSRN for: <3 useful search keywords>"
# """

# print("\n=== AFTER (with permission to not know) ===")
# print(ask(question, system=safe_system))

policy = """<policy>
1. All personal trades need pre-clearance from Compliance.
2. Approved trades must be executed within 2 business days.
3. Shares must be held for at least 30 days.
4. No trading during blackout periods before quarterly results.
</policy>"""

grounded_system = """Answer using ONLY the information in <policy>.
If the answer is not in the policy, reply exactly: "The policy does not cover this."
Do not use outside knowledge."""

for q in ["How long must I hold shares?",          # answer IS in the policy
          "Can I trade crypto?"]:                   # answer is NOT in the policy
    print(f"\nQ: {q}")
    print("A:", ask(f"{policy}\n\nQuestion: {q}", system=grounded_system))