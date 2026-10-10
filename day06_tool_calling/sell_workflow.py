"""Workflow version: CODE runs every check in a fixed order and decides.
The LLM is only used to explain the decision in friendly words."""
import ollama

from tools import BLACKOUT, RESTRICTED, get_holding

MODEL = "llama3.2"
MIN_DAYS_HELD = 30


def decide_sale(employee_id: str, ticker: str) -> tuple[str, str]:
    """Return (decision, reason). Pure Python: same input, same answer, every time."""
    t = ticker.strip().upper()
    holding = get_holding(employee_id, t)

    if holding["quantity"] == 0:
        return "REJECTED", f"You do not hold any {t} shares."
    if t in RESTRICTED:
        return "REJECTED", f"{t} is on the restricted list."
    if t in BLACKOUT:
        return "REJECTED", f"{t} is in a blackout period."
    if holding["days_held"] < MIN_DAYS_HELD:
        return "REJECTED", (f"You have held {t} for {holding['days_held']} days; "
                            f"the minimum is {MIN_DAYS_HELD}.")
    return "APPROVED", f"You have held {t} for {holding['days_held']} days and no restriction applies."


def explain(decision: str, reason: str) -> str:
    """Optional: let the LLM turn the decision into a friendly sentence. It cannot change the decision."""
    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Rewrite the compliance decision as one friendly sentence "
                                          "for the employee. Do not change the decision or the reason."},
            {"role": "user", "content": f"Decision: {decision}. Reason: {reason}"},
        ],
        options={"temperature": 0},
    )
    return response.message.content or f"{decision}: {reason}"


if __name__ == "__main__":
    for emp, tick in [("E102", "TCS"), ("E102", "WIPRO"), ("E102", "INFY")]:
        decision, reason = decide_sale(emp, tick)
        print(f"{emp} sell {tick}: {decision} | {reason}")