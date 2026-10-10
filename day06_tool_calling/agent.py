import json

import ollama

from tools import check_restricted, get_holding, is_blackout

MODEL = "llama3.2"
MAX_STEPS = 5

# Allow-list: the ONLY functions the model can trigger, by name
TOOLS = {
    "check_restricted": check_restricted,
    "is_blackout": is_blackout,
    "get_holding": get_holding,
}

SYSTEM = """You are a pre-clearance assistant for employees of an investment bank.
Use the tools to look up facts. Never guess a fact a tool can provide.

For ANY question about selling shares, you MUST call all three tools before answering:
get_holding, check_restricted and is_blackout.

For ANY questions apart from selling or buying shares, you MUST asnwer it directly without
calling the tools.

Policy:
- Restricted stocks may not be traded.
- Stocks in a blackout period may not be traded.
- Shares must be held at least 30 days before they can be sold.
Answer in 2-3 sentences and give the reason."""

TRADING_WORDS = {"buy", "sell", "shares", "stock", "restricted", "blackout", "hold", "own", "trade"}


def needs_tools(question: str) -> bool:
    """Cheap router: only offer tools for questions that look like trading questions."""
    words = set(question.lower().replace("?", " ").replace(".", " ").split())
    return bool(words & TRADING_WORDS)

def run_tool(name: str, args: dict) -> str:
    """Run one requested tool safely. Always returns text for the model."""
    if name not in TOOLS:
        return f"ERROR: unknown tool '{name}'. Available: {', '.join(TOOLS)}"
    try:
        result = TOOLS[name](**args)
    except TypeError as e:                       # wrong or missing arguments
        return f"ERROR: bad arguments for {name}: {e}"
    except Exception as e:                       # the tool itself failed
        return f"ERROR: {name} failed: {e}"
    return json.dumps(result)


def run_agent(question: str, verbose: bool = True) -> tuple[str, list[str]]:
    """Loop until the model answers without asking for tools. Returns (answer, tools_used)."""
    messages: list = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": question},
    ]
    tools_used: list[str] = []    
    tool_list = list(TOOLS.values()) if needs_tools(question) else []
    for step in range(1, MAX_STEPS + 1):
        response = ollama.chat(model=MODEL, messages=messages,
                               tools=tool_list, options={"temperature": 0})
                               
        messages.append(response.message)

        if not response.message.tool_calls:      # no tool requested -> final answer
            return response.message.content or "", tools_used

        for call in response.message.tool_calls:
            name, args = call.function.name, dict(call.function.arguments)
            result = run_tool(name, args)
            tools_used.append(name)
            if verbose:
                print(f"  step {step}: {name}({args}) -> {result}")
            messages.append({"role": "tool", "content": result, "tool_name": name})

    return "Stopped after too many steps. Sending to human REVIEW.", tools_used


if __name__ == "__main__":
    questions=["I'm employee E102. Can I sell my TCS shares today?",
    "Is RELIANCE in a blackout?",
    "I'm E102. Can I sell my WIPRO shares?",
    "Can I buy HDFCBANK?"]
    for q in questions:
        print("QUESTION:", q)
        answer, used = run_agent(q)
        print("ANSWER:", answer)
        print("TOOLS USED:", used,"\n\n")