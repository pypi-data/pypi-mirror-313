"""Basic functionality tests for Bjarkan SDK."""
import pytest
from bjarkan import BjarkanError
from .test_base import TestBase


class TestBasic(TestBase):
    @pytest.mark.asyncio
    async def test_sdk_initialization(self):
        """Test SDK initialization."""
        assert self.sdk is not None

    @pytest.mark.asyncio
    async def test_orderbook_config(self):
        """Test orderbook configuration."""
        # Test valid config
        response = await self.sdk.set_config(
            type="orderbook",
            aggregated=True,
            exchanges=["binance", "okx"],
            symbols=["BTC/USDT"],
            depth=10
        )
        await self.assert_success_response(response)

        # Test invalid config types
        with pytest.raises(BjarkanError) as exc_info:
            await self.sdk.set_config(type="invalid")
        assert "Invalid config type" in str(exc_info.value)

        # Test empty exchanges list
        with pytest.raises(BjarkanError) as exc_info:
            await self.sdk.set_config(
                type="orderbook",
                aggregated=True,
                exchanges=[],
                symbols=["BTC/USDT"],
                depth=10
            )
        assert "exchanges" in str(exc_info.value)

        # Test invalid depth
        with pytest.raises(BjarkanError) as exc_info:
            await self.sdk.set_config(
                type="orderbook",
                aggregated=True,
                exchanges=["binance"],
                symbols=["BTC/USDT"],
                depth=0
            )
        assert "depth" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_trades_config(self):
        """Test trades configuration."""
        response = await self.sdk.set_config(
            type="trades",
            exchanges=["binance", "okx"],
            symbols=["BTC/USDT"],
            size={"BTC/USDT": {"BTC": 0.001}}
        )
        await self.assert_success_response(response)