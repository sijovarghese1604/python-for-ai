Day 2: How LLMs work
Q1. Why can an LLM give a confident but wrong answer (hallucination)?

An LLM generates the most probable next tokens based on patterns it learned in training. It does not check facts. So when it lacks the right information, such as private company data or events after its training cutoff, it still produces fluent, plausible text, which can be wrong. The confident tone is just style, and it says nothing about accuracy.

How we reduce it: ground the model with RAG (real documents) or tools (real APIs), tell it to say "I don't know" when the context doesn't contain the answer, and validate the output (for example with Pydantic).

Q2. What's the difference between the context window and max_tokens?

The context window is the maximum number of tokens the model can handle in a single request. It covers everything: system prompt, chat history, documents, tool results, and the reply. It is fixed by the model.

max_tokens is a limit I set on the length of the reply only. It controls cost and response size. If the reply hits the limit, it is cut off mid-sentence.

Analogy: the context window is the whole page; max_tokens is how much space I allow for the answer at the bottom.

Q3. Why does turn 5 of a chat cost more than turn 1, even with the same question?

LLM APIs are stateless: the model has no memory between calls. To continue a conversation, the application resends the full chat history in every call. By turn 5 the input contains all earlier questions and answers, so there are more input tokens and a higher cost, even if the new question is the same size.

Say "we resend the history", never "the model remembers".

Q4. What temperature would you use for a compliance pre-clearance agent, and why?

Low, around 0 to 0.2. Temperature controls how random the choice of the next token is. Compliance decisions must be consistent (the same request gets the same result) and auditable (we can explain and reproduce why a decision was made). High temperature adds variety, which suits creative tasks like brainstorming or marketing copy, not rule-based decisions.

Q5. How would you reduce LLM cost in a production app?
Model routing: use a smaller, cheaper model for simple steps (classification, extraction) and the large model only for hard reasoning.
Trim or summarise chat history so input tokens don't grow every turn.
Prompt caching for long, repeated prompts such as the system prompt. Cached input is billed at a much lower rate.
Cap output with max_tokens, because output tokens cost several times more than input tokens.
Key facts to remember
Concept	One-line summary
Token	About 4 characters or ¾ of a word of English; the unit for cost, limits and speed
Context window	Max tokens per request, input and output together
Stateless	The model remembers nothing; the app resends the history
Roles	system = rules (developer), user = input, assistant = model's replies
Temperature	Low = consistent (business logic), high = varied (creative)
Cost	(input tokens × input price) + (output tokens × output price), priced per million tokens
Streaming	Send the reply token by token so the UI shows progress immediately