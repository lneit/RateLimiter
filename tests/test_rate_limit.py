"""Test rate_limit decorator.
"""
import pytest
from asynctest import CoroutineMock, MagicMock, patch

from decorators.rate_limit import rate_limit


@pytest.fixture
def app_context():
    """Application context fixture.
    """
    from proxy.app import PROXY

    return PROXY.app_context()


@pytest.mark.asyncio
async def test_first_time_call(app_context):
    """Test first time call. No entry in the store yet.
    """
    request = MagicMock(return_value={"headers": MagicMock()})
    with patch("decorators.rate_limit.request", request) as mock_request:
        mock_request.headers.__getitem__.return_value = "abc"
        with patch("decorators.rate_limit.RedisStore", MagicMock()) as mock_redis:
            # Mock no record in redis
            mock_redis_get = (
                mock_redis.return_value.__aenter__.return_value.get
            ) = CoroutineMock(side_effect=[None])

            mock_redis_set = (
                mock_redis.return_value.__aenter__.return_value.set
            ) = CoroutineMock()
            mock_redis_incr = (
                mock_redis.return_value.__aenter__.return_value.mock_redis_incr
            ) = CoroutineMock()

            mock_endpoint_func = CoroutineMock(side_effect=[200])

            wrapped = rate_limit(1, 5)(mock_endpoint_func)
            result = await wrapped()

            assert mock_redis.call_count == 1
            assert mock_redis_get.call_count == 1
            assert mock_redis_set.call_count == 1
            assert mock_redis_incr.call_count == 0
            assert mock_endpoint_func.call_count == 1
            assert result == 200


@pytest.mark.asyncio
async def test_rate_exceeded(app_context):
    """Test a call when the rate limit has exceeded.
    """
    request = MagicMock(return_value={"headers": MagicMock()})
    with patch("decorators.rate_limit.request", request) as mock_request:
        mock_request.headers.__getitem__.return_value = "abc"
        with patch("decorators.rate_limit.RedisStore", MagicMock()) as mock_redis:
            # Mock a record in redis with a current counter set to 1
            mock_redis_get = (
                mock_redis.return_value.__aenter__.return_value.get
            ) = CoroutineMock(side_effect=[1])

            mock_redis_set = (
                mock_redis.return_value.__aenter__.return_value.set
            ) = CoroutineMock()
            mock_redis_incr = (
                mock_redis.return_value.__aenter__.return_value.mock_redis_incr
            ) = CoroutineMock()

            mock_endpoint_func = CoroutineMock()

            wrapped = rate_limit(1, 5)(mock_endpoint_func)

            result = await wrapped()

            assert mock_redis.call_count == 1
            assert mock_redis_get.call_count == 1
            assert mock_redis_set.call_count == 0
            assert mock_redis_incr.call_count == 0
            assert mock_endpoint_func.call_count == 0
            assert result[1] == 429


@pytest.mark.asyncio
async def test_next_time_call(app_context):
    """Test a call within a good rate limit.
    """
    request = MagicMock(return_value={"headers": MagicMock()})
    with patch("decorators.rate_limit.request", request) as mock_request:
        mock_request.headers.__getitem__.return_value = "abc"
        with patch("decorators.rate_limit.RedisStore", MagicMock()) as mock_redis:
            # Mock a record in redis with a current counter set to 1
            mock_redis_get = (
                mock_redis.return_value.__aenter__.return_value.get
            ) = CoroutineMock(side_effect=[1])

            mock_redis_set = (
                mock_redis.return_value.__aenter__.return_value.set
            ) = CoroutineMock()
            mock_redis_incr = (
                mock_redis.return_value.__aenter__.return_value.incr
            ) = CoroutineMock()

            mock_endpoint_func = CoroutineMock(side_effect=[200])

            wrapped = rate_limit(2, 5)(mock_endpoint_func)

            result = await wrapped()

            assert mock_redis.call_count == 1
            assert mock_redis_get.call_count == 1
            assert mock_redis_set.call_count == 0
            assert mock_redis_incr.call_count == 1
            assert mock_endpoint_func.call_count == 1
            assert result == 200
