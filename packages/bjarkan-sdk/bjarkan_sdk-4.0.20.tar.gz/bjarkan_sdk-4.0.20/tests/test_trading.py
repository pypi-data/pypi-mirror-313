"""Trading functionality tests for Bjarkan SDK."""
import pytest
from unittest.mock import patch, MagicMock
from bjarkan import BjarkanError, OrderConfig


@pytest.mark.asyncio
async def test_order_execution(sdk, mock_api_configs, mock_orderbook_data):
    """Test order execution flow."""
    # Configure orderbook
    await sdk.set_config(
        type="orderbook",
        aggregated=True,
        exchanges=["binance"],
        symbols=["BTC/USDT"],
        depth=10
    )

    # Create order
    order = OrderConfig(
        side="buy",
        type="limit",
        time_in_force="gtc",
        amount=0.01,
        price=50000.0
    )

    # Mock the exchange's createOrder method
    with patch('ccxt.pro.binance.createOrder') as mock_create_order:
        mock_create_order.return_value = {
            "id": "test_order",
            "status": "closed",
            "filled": 0.01,
            "price": 50000.0
        }

        result = await sdk.execute_order(order, mock_api_configs)

        assert result["status"] == "completed"
        assert result["filled_amount"] == 0.01


@pytest.mark.asyncio
async def test_order_validation(sdk, mock_api_configs):
    """Test order validation."""
    # Configure orderbook
    await sdk.set_config(
        type="orderbook",
        aggregated=True,
        exchanges=["binance"],
        symbols=["BTC/USDT"],
        depth=10
    )

    # Test invalid order type
    with pytest.raises(BjarkanError):
        order = OrderConfig(
            side="buy",
            type="invalid",
            time_in_force="gtc",
            amount=0.01,
            price=50000.0
        )
        await sdk.execute_order(order, mock_api_configs)

    # Test invalid time in force
    with pytest.raises(BjarkanError):
        order = OrderConfig(
            side="buy",
            type="limit",
            time_in_force="invalid",
            amount=0.01,
            price=50000.0
        )
        await sdk.execute_order(order, mock_api_configs)


@pytest.mark.asyncio
async def test_authentication_errors(sdk, mock_api_configs):
    """Test handling of authentication errors."""
    await sdk.set_config(
        type="orderbook",
        aggregated=True,
        exchanges=["binance"],
        symbols=["BTC/USDT"],
        depth=10
    )

    order = OrderConfig(
        side="buy",
        type="limit",
        time_in_force="gtc",
        amount=0.01,
        price=50000.0
    )

    # Test invalid API credentials
    with patch('ccxt.pro.binance.createOrder') as mock_create_order:
        mock_create_order.side_effect = Exception("Invalid API Key")

        with pytest.raises(BjarkanError) as exc_info:
            await sdk.execute_order(order, mock_api_configs)

        assert "Invalid API" in str(exc_info.value)
