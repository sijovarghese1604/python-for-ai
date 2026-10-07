from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from extractor import TradeExtraction, extract
from rules import Decision, decide

app = FastAPI(title="Pre-clearance API", version="0.1.0")


# ---------- request / response models ----------
class PreClearanceRequest(BaseModel):
    employee_id: str = Field(min_length=1, examples=["E102"])
    text: str = Field(min_length=5, max_length=1000, examples=["Please buy 100 shares of TCS"])


class PreClearanceResponse(BaseModel):
    employee_id: str
    decision: Decision
    facts: TradeExtraction | None      # None when extraction failed

    # ---------- endpoints ----------
@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/pre-clearance", response_model=PreClearanceResponse)
def pre_clearance(req: PreClearanceRequest) -> PreClearanceResponse:
    try:
        trade = extract(req.text)
    except ConnectionError:
        raise HTTPException(status_code=503, detail="LLM service unavailable. Is Ollama running?")

    return PreClearanceResponse(
        employee_id=req.employee_id,
        decision=decide(trade),
        facts=trade,
    )