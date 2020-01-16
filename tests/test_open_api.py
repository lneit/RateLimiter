"""Test openapi
pytest -s test_openapi.py
"""
import pytest
from proxy.app import PROXY

@pytest.fixture(name="test_app")
def _test_app():
    return PROXY


@pytest.mark.asyncio
async def test_openapi(test_app):
    """Testing the generation of openapi.json
    """
    test_client = test_app.test_client()
    response = await test_client.get("/openapi.json")
    data = await response.get_data()
    print(data.decode())
    assert response.status_code == 200