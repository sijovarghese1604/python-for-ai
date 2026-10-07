import asyncio
import time
import httpx

# 1. Three slow "LLM calls" in parallel
async def fake_llm_call(prompt: str, seconds: float) -> str:
    await asyncio.sleep(seconds)
    return f"answer to: {prompt}"

async def run_in_parallel() -> None:
    start = time.perf_counter()
    results = await asyncio.gather(
        fake_llm_call("summarise doc", 1),
        fake_llm_call("extract fields", 1),
        fake_llm_call("classify risk", 1),
    )
    print(results)
    print(f"took {time.perf_counter() - start:.1f}s (not 3s)")

# 2. A real HTTP call — this will become an agent "tool" in Week 2
async def get_rate(base: str, target: str) -> float:
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(
            "https://api.frankfurter.dev/v1/latest",
            params={"from": base, "to": target},
        )
        resp.raise_for_status()     # raises on 4xx / 5xx
        return resp.json()["rates"][target]

async def main() -> None:
    await run_in_parallel()
    try:
        rate = await get_rate("USD", "INR")
        print(f"1 USD = {rate} INR")
    except httpx.HTTPError as e:
        print(f"request failed: {e}")

asyncio.run(main())