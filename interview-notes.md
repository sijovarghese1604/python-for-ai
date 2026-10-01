# GenAI Interview Notes

My answer bank, built while learning. Each answer is short enough to say in about 30 seconds.

---

## Day 1: How LLMs work

### Q1. Why can an LLM give a confident but wrong answer (hallucination)?

An LLM generates the most probable next tokens based on patterns it learned in training. It does not check facts. So when it lacks the right information, such as private company data or events after its training cutoff, it still produces fluent, plausible text, which can be wrong. The confident tone is just style, and it says nothing about accuracy.

**How we reduce it:** ground the model with RAG (real documents) or tools (real APIs), tell it to say "I don't know" when the context doesn't contain the answer, and validate the output (for example with Pydantic).

---

### Q2. What's the difference between the context window and `max_tokens`?

The **context window** is the maximum number of tokens the model can handle in a single request. It covers everything: system prompt, chat history, documents, tool results, and the reply. It is fixed by the model.

**`max_tokens`** is a limit I set on the length of the reply only. It controls cost and response size. If the reply hits the limit, it is cut off mid-sentence.

> Analogy: the context window is the whole page; `max_tokens` is how much space I allow for the answer at the bottom.

---

### Q3. Why does turn 5 of a chat cost more than turn 1, even with the same question?

LLM APIs are **stateless**: the model has no memory between calls. To continue a conversation, the application resends the full chat history in every call. By turn 5 the input contains all earlier questions and answers, so there are more input tokens and a higher cost, even if the new question is the same size.

> Say "we resend the history", never "the model remembers".

---

### Q4. What temperature would you use for a compliance pre-clearance agent, and why?

Low, around 0 to 0.2. Temperature controls how random the choice of the next token is. Compliance decisions must be **consistent** (the same request gets the same result) and **auditable** (we can explain and reproduce why a decision was made). High temperature adds variety, which suits creative tasks like brainstorming or marketing copy, not rule-based decisions.

**Good follow-up point:** some providers now remove this setting. Anthropic's Python SDK v1 (2026) no longer accepts `temperature`, so consistency comes from clear instructions, structured output with validation, and evals rather than one number.

---

### Q5. How would you reduce LLM cost in a production app?

1. **Model routing:** use a smaller, cheaper model for simple steps (classification, extraction) and the large model only for hard reasoning.
2. **Trim or summarise chat history** so input tokens don't grow every turn.
3. **Prompt caching** for long, repeated prompts such as the system prompt. Cached input is billed at a much lower rate.
4. **Cap output with `max_tokens`**, because output tokens cost several times more than input tokens.

---

## Day 2: Calling LLMs, local vs cloud

### Q6. How does a Python app talk to an LLM?

Through HTTP. The model runs inside a server: Ollama on my own laptop at `localhost:11434`, or a cloud API such as `api.anthropic.com`. The Python SDK (the `ollama` or `anthropic` package) is only a client that builds the HTTP request and turns the JSON reply into objects. It contains no model. I proved this by calling Ollama's `/api/chat` endpoint directly with `httpx`, without the SDK.

---

### Q7. Why does a cloud API need a key but a local Ollama server doesn't?

An API key identifies who is calling, so the provider can authorise the request and bill the right account. A local Ollama server runs on my own machine, is only reachable from my machine by default, and costs nothing per call, so there is no one to authenticate and nothing to bill. In production, a self-hosted model server would still sit behind authentication.

---

### Q8. Why might a model refuse one question but invent the answer to another?

The model never looks anything up; in both cases it simply lacks the information. What differs is the wording. A question with a specific document ID matches a pattern it was trained to refuse ("I can't access that document"). A request for a formatted list ("3 papers with authors, year and journal") pulls it toward filling the format with plausible content. So you can't rely on the model to refuse: use RAG, source verification and evals.

**My own example:** a local Llama 3.2 model refused to summarise a made-up SEBI circular number, but invented three realistic research-paper citations, with real journal names, volumes and pages, none of which exist.

---

### Q9. Local model vs cloud API: trade-offs?

| | Local (e.g. Llama 3.2 3B on Ollama) | Cloud API (e.g. Claude) |
| --- | --- | --- |
| Cost | Free per call (you pay in hardware) | Pay per token |
| Privacy | Data never leaves the machine | Data is sent to the provider |
| Quality | Smaller model: weaker reasoning and tool use, more hallucination | Much larger, more capable models |
| Speed | Limited by your hardware (my laptop: ~10–20 tokens/sec) | Usually faster, on specialised hardware |
| Scale | Limited by one machine's RAM and CPU/GPU | Scales on demand |

Local models suit privacy-sensitive data, offline use and cheap experiments; cloud APIs suit production quality and scale. Many teams use both, routing tasks by sensitivity and difficulty.

---

## Key facts to remember

| Concept | One-line summary |
| --- | --- |
| Token | About 4 characters or ¾ of a word of English; the unit for cost, limits and speed |
| Context window | Max tokens per request, input and output together |
| Stateless | The model remembers nothing; the app resends the history |
| Roles | `system` = rules (developer), `user` = input, `assistant` = model's replies |
| Temperature | Low = consistent (business logic), high = varied (creative) |
| Cost | (input tokens × input price) + (output tokens × output price), priced per million tokens |
| Streaming | Send the reply token by token so the UI shows progress immediately |
