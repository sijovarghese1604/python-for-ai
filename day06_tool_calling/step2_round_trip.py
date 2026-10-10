import ollama

from tools import check_restricted

MODEL = "llama3.2"

messages: list = [{"role": "user", "content": "Is INFY on the restricted list?"}]
# messages: list = [{"role": "user", "content": "What is the capital of France?"}]
# messages: list = [{"role": "system", "content":
#         "You help bank employees with trading compliance. Only use a tool when the question "
#         "is about a specific stock. For any other question, answer directly without tools."},
#     {"role": "user", "content": "What is the capital of France?"},
# ]

# 1. First call: the model asks for a tool
response = ollama.chat(model=MODEL, messages=messages, tools=[check_restricted],
                       options={"temperature": 0})
messages.append(response.message)        # keep the model's request in the history

# 2. YOUR code runs each requested tool and adds the result to the history
for call in response.message.tool_calls or []:
    result = check_restricted(**call.function.arguments)
    print(f"ran {call.function.name}({call.function.arguments}) -> {result}")
    messages.append({"role": "tool", "content": str(result), "tool_name": call.function.name})

# 3. Second call: the model sees the result and writes the answer
final = ollama.chat(model=MODEL, messages=messages, tools=[check_restricted],
                    options={"temperature": 0})
print("ANSWER:", final.message.content)