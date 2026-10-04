from extractor import TradeExtraction

RESTRICTED = {"INFY", "HDFCBANK"}
REVIEW_ABOVE = 10_000

# Company names people actually type -> official ticker
ALIASES = {
    "INFOSYS": "INFY",
    "HDFC BANK": "HDFCBANK",
    "HDFC": "HDFCBANK",
    "TATA MOTORS": "TATAMOTORS",
}


def normalize(ticker: str) -> str:
    t = ticker.strip().upper()
    return ALIASES.get(t, t)


def decide(trade: TradeExtraction | None) -> str:
    if trade is None:                      # extraction failed twice -> a human looks at it
        return "REVIEW"
    if normalize(trade.ticker) in RESTRICTED:
        return "REJECTED"
    if trade.blackout_period:
        return "REJECTED"
    if trade.quantity > REVIEW_ABOVE:      # more than 10,000; exactly 10,000 is fine
        return "REVIEW"
    return "APPROVED"

if __name__ == "__main__":
    t = TradeExtraction(ticker="Infosys", action="buy", quantity=5, blackout_period=False)
    print(decide(t))                       # REJECTED (alias -> INFY)
    t = TradeExtraction(ticker="IDFC", action="buy", quantity=10_000, blackout_period=False)
    print(decide(t))                       # APPROVED (exactly 10,000)
    t = TradeExtraction(ticker="IDFC", action="buy", quantity=10_001, blackout_period=False)
    print(decide(t))                       # REVIEW
    print(decide(None))                    # REVIEW (extraction failed)