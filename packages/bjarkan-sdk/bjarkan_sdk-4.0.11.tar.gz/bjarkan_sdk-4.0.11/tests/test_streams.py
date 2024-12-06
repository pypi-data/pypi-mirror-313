"""Stream management tests for Bjarkan SDK."""
import pytest
import asyncio
from unittest.mock import patch, AsyncMock
from bjarkan import BjarkanError
from .test_base import TestBase


class TestStreams(TestBase):
    @pytest.mark.asyncio
    @patch('ccxt.pro.binance')
    async def test_stream_lifecycle(self, mock_exchange):
        """Test complete stream lifecycle."""
        # Setup mock exchange
        mock_exchange.return_value = AsyncMock()
        mock_exchange.return_value.watchOrderBook = AsyncMock(return_value={
            "bids": [[50000, 1.0]],
            "asks": [[50001, 1.0]],
            "timestamp": 1638338400000,
        })

        # Configure stream
        await self.sdk.set_config(
            type="orderbook",
            aggregated=True,
            exchanges=["binance"],
            symbols=["BTC/USDT"],
            depth=10
        )

        # Start stream
        response = await self.sdk.start_stream("orderbook")
        await self.assert_success_response(response)

        # Give some time for data collection
        await asyncio.sleep(0.1)

        # Get data
        data = await self.sdk.get_latest_data("orderbook")
        assert "BTC/USDT" in data

        # Stop stream
        response = await self.sdk.stop_stream("orderbook")
        await self.assert_success_response(response)

    @pytest.mark.asyncio
    @patch('ccxt.pro.binance')
    async def test_multiple_streams(self, mock_exchange):
        """Test running multiple streams simultaneously."""
        # Setup mock exchange
        mock_exchange.return_value = AsyncMock()
        mock_exchange.return_value.watchOrderBook = AsyncMock(return_value={
            "bids": [[50000, 1.0]],
            "asks": [[50001, 1.0]],
            "timestamp": 1638338400000,
        })
        mock_exchange.return_value.watchTrades = AsyncMock(return_value=[{
            "id": "1",
            "price": 50000,
            "amount": 1.0,
            "side": "buy",
            "timestamp": 1638338400000,
        }])

        # Configure both streams
        await self.sdk.set_config(
            type="orderbook",
            aggregated=True,
            exchanges=["binance"],
            symbols=["BTC/USDT"],
            depth=10
        )

        await self.sdk.set_config(
            type="trades",
            exchanges=["binance"],
            symbols=["BTC/USDT"]
        )

        # Start both streams
        await self.sdk.start_stream("orderbook")
        await self.sdk.start_stream("trades")

        # Give some time for data collection
        await asyncio.sleep(0.1)

        # Get data
        orderbook_data = await self.sdk.get_latest_data("orderbook")
        trades_data = await self.sdk.get_latest_data("trades")

        assert "BTC/USDT" in orderbook_data
        assert "binance" in trades_data

        # Stop streams
        await self.sdk.stop_stream("orderbook")
        await self.sdk.stop_stream("trades")

    @pytest.mark.asyncio
    @patch('ccxt.pro.binance')
    async def test_stream_callbacks(self, mock_exchange):
        """Test stream callbacks."""
        callback_data = []

        async def test_callback(data):
            callback_data.append(data)

        # Setup mock exchange
        mock_exchange.return_value = AsyncMock()
        mock_exchange.return_value.watchOrderBook = AsyncMock(return_value={
            "bids": [[50000, 1.0]],
            "asks": [[50001, 1.0]],
            "timestamp": 1638338400000,
        })

        # Configure and start stream with callback
        await self.sdk.set_config(
            type="orderbook",
            aggregated=True,
            exchanges=["binance"],
            symbols=["BTC/USDT"],
            depth=10
        )

        await self.sdk.start_stream("orderbook", callback=test_callback)
        await asyncio.sleep(0.1)  # Give callback time to execute
        await self.sdk.stop_stream("orderbook")

        assert len(callback_data) > 0
        assert "symbol" in callback_data[0]
        assert callback_data[0]["symbol"] == "BTC/USDT"