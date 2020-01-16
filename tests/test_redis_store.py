"""Test Redis store context manager.
"""
import pytest
from asynctest import CoroutineMock, MagicMock, patch

from store.redis_store import RedisStore


@pytest.mark.asyncio
async def test_redis_store_context_manager():
    """Test redis store context manager
    """
    mock_redis = CoroutineMock(return_value={"close": MagicMock()})
    mock_create_redis = CoroutineMock(side_effect=[mock_redis])
    with patch("store.redis_store.create_redis", mock_create_redis):
        async with RedisStore("localhost"):
            assert mock_create_redis.call_count == 1
