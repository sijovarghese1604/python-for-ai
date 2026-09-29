# Python for AI Engineering

Learning log for my transition from Frontend Tech Lead to GenAI Application Engineer.

## Day 1
- `basics.py`, `types_demo.py`: Python syntax, type hints, dataclasses
- `pydantic_demo.py`: runtime validation of LLM-style JSON output
- `exercise.py`: async trade pre-clearance checker. Validates requests with
  Pydantic, checks a restricted list, and processes all requests in parallel
  with `asyncio.gather`.