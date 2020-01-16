"""Test App client. This integration test expects Redis to run as a daemon process.
pytest -s tests/test_app.py
"""
import pytest


@pytest.fixture()
def test_app(monkeypatch):
    """App fixture.
    """
    monkeypatch.setenv("REQUEST_COUNT", "1")
    monkeypatch.setenv("INTERVAL", "5")
    from proxy.app import PROXY

    return PROXY


@pytest.mark.asyncio
async def test_get(test_app):
    """Testing GET request. The rate is limited to 1 request per 5 secs
    (See environment mocks in app fixture).
    """
    test_client = test_app.test_client()
    response_1 = await test_client.get("/")
    response_2 = await test_client.get("/")
    response_3 = await test_client.get("/")
    assert response_1.status_code == 200
    assert response_2.status_code == 429
    assert response_3.status_code == 429
