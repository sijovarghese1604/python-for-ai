import asyncio
import time

from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/bad")            # async def + a BLOCKING wait
async def bad():
    time.sleep(5)           # like ollama.chat(): no await, holds the event loop
    return {"done": "bad"}


@app.get("/good-thread")    # plain def + blocking wait -> runs in a thread
def good_thread():
    time.sleep(5)
    return {"done": "good-thread"}


@app.get("/good-async")     # async def + an AWAITABLE wait
async def good_async():
    await asyncio.sleep(5)  # like await AsyncClient().chat(): gives control back
    return {"done": "good-async"}