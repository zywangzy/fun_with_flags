"""Integration test for Redis Gateway."""
from datetime import timedelta
import pytest
from time import sleep


@pytest.mark.usefixtures("redis_gateway")
def test_create_redis_gateway(redis_gateway):
    assert redis_gateway is not None


@pytest.mark.usefixtures("redis_gateway")
@pytest.mark.parametrize("name,value,ex",
                         [
                             ("testname1", "value1", timedelta(seconds=1)),
                             ("testname2", "value2", None),
                             ("testname2", "value3", None),
                         ])
def test_set(redis_gateway, name, value, ex):
    redis_gateway.set(name, value, ex)


@pytest.mark.usefixtures("redis_gateway")
@pytest.mark.parametrize("name,expected", [("wrongName", None), ("testname1", "value1"), ("testname2", "value3")])
def test_get(redis_gateway, name, expected):
    # When & Then
    if expected:
        assert expected == redis_gateway.get(name)
    else:
        assert redis_gateway.get(name) is expected


@pytest.mark.usefixtures("redis_gateway")
def test_get_expired(redis_gateway):
    # Sleep to make the key expire
    sleep(1)
    # Given
    name = "testname1"
    # When & Then
    assert redis_gateway.get(name) is None
