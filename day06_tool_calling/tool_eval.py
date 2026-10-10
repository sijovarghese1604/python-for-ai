from agent import run_agent

# question, tools that must be used, words the answer MUST contain, words it must NOT contain
CASES = [
    ("Is INFY on the restricted list?", {"check_restricted"}, ["restricted"], []),
    ("Is RELIANCE in a blackout period right now?", {"is_blackout"}, ["blackout"], []),
    ("I'm employee E102. How many TCS shares do I own?", {"get_holding"}, ["200"], []),
    ("I'm employee E102. Can I sell my TCS shares today?", {"get_holding"}, ["12", "30"], ["you can sell"]),
    ("What does pre-clearance mean?", set(), [], []),
]

passed = 0
for question, required, must_have, must_not in CASES:
    answer, used = run_agent(question, verbose=False)
    tools_ok = required <= set(used) if required else not used
    text = answer.lower()
    answer_ok = all(w.lower() in text for w in must_have) and not any(w.lower() in text for w in must_not)
    ok = tools_ok and answer_ok
    passed += ok
    print(f"{'PASS' if ok else 'FAIL'}  tools_ok={tools_ok} answer_ok={answer_ok}  used={used}\n      Q: {question}\n      A: {answer}\n")

print(f"Score: {passed}/{len(CASES)}")