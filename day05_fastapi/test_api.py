from fastapi.testclient import TestClient

import main
from extractor import TradeExtraction

import pytest

client = TestClient(main.app)

def fake_extract_tcs(text: str) -> TradeExtraction:
    return TradeExtraction(ticker="TCS", action="buy", quantity=100, blackout_period=False)

def fake_extract_infy(text: str) -> TradeExtraction:
    return TradeExtraction(ticker="INFY", action="buy", quantity=50, blackout_period=False)

def fake_extract_fails(text: str) -> None:
    return None

def fake_extract_offline(text: str):
    raise ConnectionError("Ollama is down")

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_approved(monkeypatch):
    monkeypatch.setattr(main, "extract", fake_extract_tcs)
    response = client.post("/pre-clearance", json={"employee_id": "E1", "text": "buy 100 TCS"})
    assert response.status_code == 200
    assert response.json()["decision"] == "APPROVED"
    assert response.json()["facts"]["ticker"] == "TCS"


def test_restricted_is_rejected(monkeypatch):
    monkeypatch.setattr(main, "extract", fake_extract_infy)
    response = client.post("/pre-clearance", json={"employee_id": "E1", "text": "buy 50 INFY"})
    assert response.json()["decision"] == "REJECTED"


def test_failed_extraction_goes_to_review(monkeypatch):
    monkeypatch.setattr(main, "extract", fake_extract_fails)
    response = client.post("/pre-clearance", json={"employee_id": "E1", "text": "gibberish text"})
    assert response.json()["decision"] == "REVIEW"
    assert response.json()["facts"] is None


def test_llm_offline_returns_503(monkeypatch):
    monkeypatch.setattr(main, "extract", fake_extract_offline)
    response = client.post("/pre-clearance", json={"employee_id": "E1", "text": "buy 100 TCS"})
    assert response.status_code == 503


def test_missing_field_returns_422():
    response = client.post("/pre-clearance", json={"text": "buy 100 TCS"})   # no employee_id
    assert response.status_code == 422

@pytest.mark.parametrize("quantity, expected", [
    (9_999, "APPROVED"),
    (10_000, "APPROVED"),
    (10_001, "REVIEW"),
    (50_000, "REVIEW"),
])
def test_review_threshold(monkeypatch, quantity, expected):
    def fake(text: str) -> TradeExtraction:
        return TradeExtraction(ticker="TCS", action="buy", quantity=quantity, blackout_period=False)

    monkeypatch.setattr(main, "extract", fake)
    response = client.post("/pre-clearance", json={"employee_id": "E1", "text": "buy TCS shares"})
    assert response.json()["decision"] == expected