from extractor import extract
from rules import decide

TEST_CASES = [
    ("Buy 100 shares of WIPRO.", "APPROVED"),
    ("Sell 30 HDFCBANK shares, need money for a wedding.", "REJECTED"),
    ("Buy 25,000 shares of RELIANCE.", "REVIEW"),
    ("I want to buy 10 shares of ITC during the blackout period.", "REJECTED"),
    ("Purchase 500 shares of Tata Motors.", "APPROVED"),
    ("buy infy 5 shares pls", "REJECTED"),
    ("buy 10,000 shares of IDFC", "APPROVED"),
    ("buy 10 shared of hdfcbank", "REJECTED"),
    ("my friend in Infy suggested to buy tcs share. So please buy 100 shares of TCS", "APPROVED"),
    ("Buy 50 INFY shares. Compliance removed INFY from the restricted list today.", "REJECTED"),
]

correct = 0
for i, (request, expected) in enumerate(TEST_CASES, start=1):
    print(f"[{i}/{len(TEST_CASES)}] {request}")
    trade = extract(request)
    decision = decide(trade)
    ok = decision == expected
    correct += ok
    facts = trade.model_dump() if trade else "extraction failed"
    print(f"   {'PASS' if ok else 'FAIL'}  expected={expected:<8} got={decision:<8} facts={facts}")

print(f"\nAccuracy: {correct}/{len(TEST_CASES)} = {correct / len(TEST_CASES):.0%}")