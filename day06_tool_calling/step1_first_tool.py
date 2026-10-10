import ollama

from tools import check_restricted

MODEL = "llama3.2"

response = ollama.chat(
    model=MODEL,
    messages=[{"role": "user", "content": "Is INFY on the restricted list?"}],
    # messages=[{"role": "user", "content": "What is the capital of France?"}],
#     messages=[
#     {"role": "system", "content":
#         "You help bank employees with trading compliance. Only use a tool when the question "
#         "is about a specific stock. For any other question, answer directly without tools."},
#     {"role": "user", "content": "What is the capital of France?"},
# ],
    tools=[check_restricted],            # <-- the menu of functions the model may ask for
    options={"temperature": 0},
)

print("TEXT:", repr(response.message.content))
print("TOOL CALLS:", response.message.tool_calls)

for call in response.message.tool_calls or []:
    print("  model wants:", call.function.name, "with", call.function.arguments)