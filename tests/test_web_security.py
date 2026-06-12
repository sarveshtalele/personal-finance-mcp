"""Security regression tests for the web/API layer."""

import pytest
from starlette.testclient import TestClient

from src.web import server
from src.web.server import app


@pytest.fixture(autouse=True)
def _reset_rate_limiter():
    server._hits.clear()
    yield
    server._hits.clear()


@pytest.fixture
def client():
    return TestClient(app)


def test_security_headers_present(client):
    r = client.get("/api/health")
    assert r.headers["x-content-type-options"] == "nosniff"
    assert "content-security-policy" in r.headers
    assert "strict-transport-security" in r.headers


def test_calc_valid(client):
    r = client.post(
        "/api/calc",
        json={
            "calculator": "emi",
            "params": {"principal": 5_000_000, "annual_rate": 8.5, "tenure_years": 20},
        },
    )
    assert r.status_code == 200
    assert round(r.json()["result"]["emi"], 2) == 43391.16


def test_calc_rejects_unbounded_years(client):
    # DoS guard: loop-driving input over the cap must be rejected, not executed.
    r = client.post(
        "/api/calc",
        json={
            "calculator": "epf",
            "params": {"monthly_basic": 50000, "years": 99_999_999},
        },
    )
    assert r.status_code == 400


def test_calc_rejects_non_finite(client):
    # Send raw JSON so the non-finite value reaches the server (json= can't encode inf).
    r = client.post(
        "/api/calc",
        content=b'{"calculator":"future_value","params":{"present_value":1e400}}',
        headers={"content-type": "application/json"},
    )
    assert r.status_code == 400


def test_calc_unknown_calculator(client):
    r = client.post("/api/calc", json={"calculator": "../etc/passwd", "params": {}})
    assert r.status_code == 400


def test_quote_rejects_bad_symbol(client):
    assert client.get("/api/quote?symbol=../secret").status_code == 400


def test_fx_rejects_bad_currency(client):
    assert client.get("/api/fx?base=US$&symbols=INR").status_code == 400


def test_nav_rejects_bad_code(client):
    assert client.get("/api/nav?code=abc").status_code == 400


def test_oversized_body_rejected(client):
    big = {"calculator": "emi", "params": {"x": "a" * 20000}}
    r = client.post("/api/calc", json=big)
    assert r.status_code in (400, 413)


def test_rate_limit_triggers(client):
    statuses = [
        client.get("/api/health").status_code for _ in range(server.RATE_LIMIT + 5)
    ]
    assert 429 in statuses
