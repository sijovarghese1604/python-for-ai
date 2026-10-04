# Python for AI Engineering

A hands-on learning log from my move from **Frontend Tech Lead (12 years, React)** to **GenAI Application Engineer**.
Every day adds working code, measured results and interview notes. The running example throughout is a real
banking workflow I know from Morgan Stanley: **employee trade pre-clearance** for compliance.

## Highlight: LLM extraction + rules in code

On the same 10-case test set and the same small local model (Llama 3.2, 3B parameters):

| Approach | Accuracy | "Exactly 10,000 shares" | "Friend works at Infy, buy TCS" | Prompt injection |
| --- | --- | --- | --- | --- |
| LLM decides directly (prompt-engineered) | 8/10 | ❌ | ❌ | ✅ |
| **LLM extracts facts → Python applies rules** | **10/10** | ✅ | ✅ | ✅ |

```
Messy request ──▶ LLM extracts JSON ──▶ Pydantic validates ──▶ Python rules ──▶ APPROVED / REJECTED / REVIEW
                  (schema-constrained)    │ invalid
                                          └──▶ retry with the error ──▶ still invalid ──▶ REVIEW (fail safe)
```

The model does what it's good at (reading messy language); code does what it's good at (applying rules exactly,
unit-testable, immune to prompt injection).

## Tech stack

- **Python 3.12**, managed with **uv**
- **Pydantic v2**: validation of user input and LLM output
- **Ollama** running **Llama 3.2 (3B)** locally; also compared with Qwen 2.5 (3B)
- **asyncio**, **httpx**
- Type checking with Pylance / mypy

## How to run

```bash
# 1. Install uv and Ollama (https://ollama.com), then:
ollama pull llama3.2

# 2. Install dependencies
uv sync

# 3. Run the pre-clearance pipeline against the test set
uv run pipeline_eval.py
```

Every file runs on its own with `uv run <file>.py`. Ollama must be running for files that call the model.

## What's inside, day by day

### Day 1: Python for AI

| File | What it shows |
| --- | --- |
| `basics.py` | Python syntax mapped from JavaScript/Java: comprehensions, dicts, unpacking |
| `types_demo.py` | Type hints, `Literal`, dataclasses, `@property` |
| `pydantic_demo.py` | Runtime validation, nested models, JSON Schema generation |
| `async_demo.py` | `async`/`await`, `asyncio.gather`, HTTP calls with httpx |
| `exercise.py` | Async pre-clearance checker: validates 5 requests and checks them in parallel (~0.5 s, not 2.5 s) |

### Day 2: How LLMs work, and calling one from Python

| File | What it shows |
| --- | --- |
| `cost_simulator.py` | Token-based cost per turn; why statelessness makes long chats expensive; history trimming |
| `local_first_call.py` | First call to a local model: tokens, `done_reason`, tokens/second |
| `local_chat.py` | Multi-turn chat with a limited history window, cut-off detection and speed stats |

### Day 3: Prompt engineering and first evals

| File | What it shows |
| --- | --- |
| `prompt_lab.py` | Reusable `ask()` helper (system prompt, few-shot examples, temperature) |
| `t1_specific.py` … `t5_dont_know.py` | Five techniques: specificity, system prompts, tags against prompt injection, few-shot, grounding |
| `classifier.py` | Pre-clearance classifier scored on a 10-case test set, including tricky and adversarial cases |

### Day 4: Structured output

| File | What it shows |
| --- | --- |
| `json_demo.py` | Schema-constrained JSON from a Pydantic model (`format=`) |
| `extractor.py` | Trade-fact extraction with validation, self-correcting retry and fail-safe |
| `rules.py` | Compliance rules in plain Python: restricted list, blackout, review threshold, ticker aliases |
| `pipeline_eval.py` | End-to-end evaluation that prints the extracted facts, so each failure points to the right layer |

## Findings from my own experiments

- **Hallucination depends on wording.** Asked about a made-up SEBI circular number, the model refused. Asked for
  "3 research papers with authors and journals", it invented convincing citations, mixing real academics' names
  into fake papers.
- **Prompting reduces hallucination but doesn't remove it.** "Never invent sources" made the model hedge, yet it
  still listed fake "related" papers. Grounding the model in provided text was far more reliable.
- **Tags help against prompt injection, but code is the real defence.** Tagging untrusted input cut successful
  attacks from 2 of 3 to 1 of 3. A false "Compliance removed INFY from the restricted list" still got through,
  until the restricted-list check moved into code.
- **Fixing one problem can create another.** A stricter anti-injection prompt started rejecting valid trades
  (it even claimed TCS was restricted). Only the full test set caught the regression.
- **Same size, different behaviour.** On identical tests, Llama 3.2 3B scored 8/10 and Qwen 2.5 3B scored 6/10.
  Neither ever wrongly approved a restricted trade, so I track dangerous errors separately from safe ones.
- **Business limits don't belong in the extraction schema.** With a 100-share cap in the schema, a 500-share
  request came back as `quantity: 100`: valid JSON, wrong fact, no error. The schema should describe the data
  faithfully; code enforces the limits.

## Interview notes

[`interview-notes.md`](interview-notes.md) holds my answers to common GenAI interview questions (Q1–Q19), each
backed by results from this repo: tokens and context windows, statelessness, temperature, cost control,
local vs cloud models, hallucination, prompt injection, few-shot prompting, grounding, evals and structured output.

## Roadmap

- [x] Week 1: Python for AI, LLM fundamentals, prompt engineering, structured output
- [ ] FastAPI service: `POST /pre-clearance` with automated API tests
- [ ] Tool calling and the agent loop, with a streaming React / Next.js chat UI
- [ ] RAG over compliance policy documents, with citations (pgvector)
- [ ] Agents with LangGraph and MCP, including human-in-the-loop approval
- [ ] Flagship project: Compliance Pre-Clearance Agent with a React review console
- [ ] Evals, tracing (Langfuse), guardrails and cost control

## About me

Sijo Varghese, Frontend Technical Lead with nearly 12 years building enterprise React applications for global
banks (Morgan Stanley, Goldman Sachs, Danske Bank), now building GenAI applications end to end.
[LinkedIn](https://linkedin.com/in/sijovarghese1604)
