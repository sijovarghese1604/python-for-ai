import ollama

MODEL = "llama3.2"
SYSTEM = "You are a friendly compliance assistant. Keep answers under 4 sentences."
MAX_HISTORY = 7  # how many recent messages to send (besides the system prompt)

history: list[dict] = [{"role": "system", "content": SYSTEM}]

while True:
    user_text = input("\nYou: ")
    if user_text.strip().lower() in {"quit", "exit"}:
        break

    history.append({"role": "user", "content": user_text})
    to_send = [history[0], *history[1:][-MAX_HISTORY:]]
    response = ollama.chat(
        model=MODEL,
        # messages=history,                         # send the WHOLE history every time
        # messages=[history[0], history[-1]],       # only the system prompt + latest message
        messages=to_send,                           # only the system prompt + last 6 messages
        options={"num_predict": 400, "temperature": 0.3},
    )

    reply = response.message.content
    history.append({"role": "assistant", "content": reply})   # save it for next turn

    print(f"\nAssistant: {reply}")
    print(f"[input={response.prompt_eval_count} output={response.eval_count} "
          f"stored={len(history)} sent={len(to_send)}]")
    if response.done_reason == "length":
        print("\nReply was cut off")
    if response.eval_duration and response.eval_count:
        seconds = response.eval_duration/1_000_000_000
        print(f"Speed : {response.eval_count/seconds:.2f} tokens/sec")
    