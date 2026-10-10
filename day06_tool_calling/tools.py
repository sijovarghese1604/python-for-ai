"""Fake company data + the functions (tools) the model may ask to use."""

RESTRICTED = {"INFY", "HDFCBANK"}
BLACKOUT = {"RELIANCE"}                     # companies about to announce results
HOLDINGS = {                                # (employee_id, ticker) -> what they own
    ("E102", "TCS"): {"quantity": 200, "days_held": 12},
    ("E102", "WIPRO"): {"quantity": 50, "days_held": 90},
}

def check_restricted(ticker: str) -> str:
    """Check ONLY whether a stock is on the restricted list. This alone is not enough to approve a sale.

    Args:
        ticker: Stock symbol, for example TCS or INFY.

    Returns:
        A sentence saying whether the stock is restricted.
    """
    t = ticker.strip().upper()
    if not t.isalpha() or t in {"NONE", "NULL", "N/A", ""}:
        return "ERROR: no valid stock ticker given. Answer the user's question directly without tools."
    if t in RESTRICTED:
        return f"{t} IS on the restricted list. Employees may not trade it."
    return f"{t} is NOT on the restricted list."

def is_blackout(ticker: str) -> bool:
    """Check whether a stock is in a blackout period (no trading before results).

    Args:
        ticker: Stock symbol, for example RELIANCE.

    Returns:
        True if trading is currently blocked by a blackout period.
    """
    return ticker.strip().upper() in BLACKOUT


def get_holding(employee_id: str, ticker: str) -> dict:
    """REQUIRED for every question about selling shares. Returns how many shares the employee owns and how many days they have held them.

    Args:
        employee_id: Employee ID, for example E102.
        ticker: Stock symbol, for example TCS.

    Returns:
        A dict with 'quantity' and 'days_held' (both 0 if the employee owns none).
    """
    key = (employee_id.strip().upper(), ticker.strip().upper())
    return HOLDINGS.get(key, {"quantity": 0, "days_held": 0})