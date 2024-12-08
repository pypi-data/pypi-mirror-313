"""Test configuration and fixtures for Bjarkan SDK."""
import pytest
import asyncio
from bjarkan import BjarkanSDK

@pytest.fixture
async def sdk():
    """Provide a fresh SDK instance for each test."""
    sdk_instance = BjarkanSDK()
    yield sdk_instance
    await sdk_instance.close()

@pytest.fixture
def event_loop():
    """Create an event loop for each test."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def mock_orderbook_data():
    """Provide sample orderbook data for testing."""
    return {
        "BTC/USDT": {
            "symbol": "BTC/USDT",
            "timestamp": 1638338400000,
            "datetime": "2024-12-05T00:00:00.000Z",
            "bids": [
                [50000.0, 1.5, "binance"],
                [49999.0, 2.0, "okx"],
                [49998.0, 1.0, "kraken"]
            ],
            "asks": [
                [50001.0, 1.0, "binance"],
                [50002.0, 2.0, "okx"],
                [50003.0, 1.5, "kraken"]
            ]
        }
    }

@pytest.fixture
def mock_trades_data():
    """Provide sample trades data for testing."""
    return {
        "binance": {
            "BTC/USDT": [
                {
                    "id": "123",
                    "timestamp": 1638338400000,
                    "datetime": "2024-12-05T00:00:00.000Z",
                    "price": 50000.0,
                    "amount": 1.0,
                    "side": "buy"
                }
            ]
        }
    }

@pytest.fixture
def mock_api_configs():
    """Provide sample API configurations for testing."""
    from bjarkan import APIConfig
    return [
        APIConfig(
            exchange="binance",
            api_key="test_key",
            secret="test_secret"
        ),
        APIConfig(
            exchange="okx",
            api_key="test_key",
            secret="test_secret",
            password="test_pass"
        )
    ]
