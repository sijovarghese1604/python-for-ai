import json
from typing import Literal
from pydantic import BaseModel, Field, ValidationError, field_validator

class Employee(BaseModel):
    id: str
    department: str
    
class TradeRequest(BaseModel):
    # employee_id: str
    employee : Employee #new
    ticker: str = Field(description="Stock symbol, e.g. INFY")
    action: Literal["buy", "sell"]
    quantity: int = Field(gt=0)
    reason: str | None = None
    price_limit: float | None = Field(default=None, gt=0) # new

    @field_validator("ticker")
    @classmethod
    def upper_ticker(cls, v: str) -> str:
        return v.strip().upper()

# 1. Pretend this JSON came back from an LLM
# llm_output = '{"employee_id": "E102", "ticker": " infy ", "action": "buy", "quantity": "50"}'
# req = TradeRequest.model_validate_json(llm_output)
# print(req)               # ticker='INFY', quantity=50 (string "50" converted to int)
# print(req.model_dump())  # back to a plain dict

# 2. Bad LLM output -> precise errors
# bad = '{"employee_id": "E102", "ticker": "TCS", "action": "hold", "quantity": -5}'
# try:
#     TradeRequest.model_validate_json(bad)
# except ValidationError as e:
#     for err in e.errors():
#         print(err["loc"], err["msg"])
# ('action',) Input should be 'buy' or 'sell'
# ('quantity',) Input should be greater than 0

# 3. JSON Schema you will give the LLM as the required format
# print(json.dumps(TradeRequest.model_json_schema(), indent=2))

good = '{"employee": {"id": "E102", "department": "Equities"}, "ticker": "infy", "action": "buy", "quantity": 50, "price_limit": 1850.5}'
req = TradeRequest.model_validate_json(good)
print(req)              
print(req.employee.department)      # Equities

# 2. No price_limit -> fine, becomes None
no_limit = '{"employee": {"id": "E103", "department": "Tax"}, "ticker": "tcs", "action": "sell", "quantity": 10}'
print(TradeRequest.model_validate_json(no_limit).price_limit)   # None

# 3. Missing department + negative price_limit -> 2 errors
bad = '{"employee": {"id": "E104"}, "ticker": "wipro", "action": "buy", "quantity": 5, "price_limit": -10}'
try:
    TradeRequest.model_validate_json(bad)
except ValidationError as e:
    for err in e.errors():
        print(err["loc"], err["msg"])
