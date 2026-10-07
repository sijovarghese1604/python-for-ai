import asyncio
from typing import Literal
import json
from pydantic import BaseModel, Field, ValidationError, field_validator


# 1. Defines TradeRequest (employee_id, ticker, action buy/sell, quantity > 0; ticker trimmed and upper-cased)
# 2. Defines Decision (employee_id, ticker, status approved / rejected / invalid, reason)
# 3. Has an async check_restricted(ticker) tool that waits 0.5 s (a fake DB call) and checks the RESTRICTED set
# 4. Has an async process(raw) -> Decision: invalid JSON fields → invalid with the Pydantic error message; restricted → rejected; otherwise approved
# 5. Processes all 5 requests in parallel with asyncio.gather — the total should take about 0.5 s, not 2.5 s

RESTRICTED = {"INFY", "HDFCBANK"}

RAW = [
    '{"employee_id": "E101", "ticker": "tcs", "action": "buy", "quantity": 100}',
    '{"employee_id": "E102", "ticker": "INFY", "action": "sell", "quantity": 20}',
    '{"employee_id": "E103", "ticker": "wipro", "action": "hold", "quantity": 10}',
    '{"employee_id": "E104", "ticker": "RELIANCE", "action": "buy", "quantity": 0}',
    '{"employee_id": "E105", "ticker": " hdfcbank ", "action": "buy", "quantity": "5"}',
]

# TODO: TradeRequest model
class TradeRequest(BaseModel):
    employee_id: str
    ticker: str = Field(description="Stock Symbol, e.g. INFY")
    action: Literal["buy","sell"]
    quantity: int = Field(gt=0)

    @field_validator("ticker")
    @classmethod
    def upper_ticker(cls, v: str)->str:
        return v.strip().upper()

# TODO: Decision model
class Decision(BaseModel):
    employee_id: str
    ticker: str= Field(description="Stock Symbol, e.g. INFY")
    status: Literal["approved","rejected","invalid"]
    reason : str | None = None 

# TODO: async check_restricted(ticker)
async def check_restricted(ticker: str)->bool:
    await asyncio.sleep(0.5)
    return ticker in RESTRICTED

async def process(raw: str) -> Decision:
    try:
        req = TradeRequest.model_validate_json(raw)
    except ValidationError as e:
        data = json.loads(raw)
        error_reason = "; ".join(f"{err['loc'][0]}: {err['msg']}" for err in e.errors())
        return Decision(
            employee_id=data["employee_id"],
            ticker=data["ticker"].strip().upper(),   # "wipro" -> "WIPRO"
            status="invalid",
            reason=error_reason,
        )

    if await check_restricted(req.ticker):
        return Decision(employee_id=req.employee_id, ticker=req.ticker,
                        status="rejected", reason="On restricted list")
    return Decision(employee_id=req.employee_id, ticker=req.ticker,
                    status="approved", reason="Passed checks")   


async def main() -> None:
    tasks = [process(r) for r in RAW]      # 5 coroutines, not started yet
    decisions = await asyncio.gather(*tasks)

    for d in decisions:
        print(f"{d.employee_id} {d.ticker:<9} {d.status:<9} {d.reason}")
    assert [d.status for d in decisions] == [
        "approved", "rejected", "invalid", "invalid", "rejected"
    ]
    print("All checks passed")

asyncio.run(main())