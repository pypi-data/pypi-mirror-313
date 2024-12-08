import asyncio
from typing import Dict, List, Optional, Callable
from bjarkan.utils.logger import logger, catch_exception
import ccxt.pro as ccxt

from bjarkan.models import OrderbookConfig, TradesConfig, APIConfig, OrderConfig
from bjarkan.core.orderbook import OrderbookManager
from bjarkan.core.trades import TradesManager
from bjarkan.core.executor import OrderExecutor
from bjarkan.exceptions import BjarkanError


class BjarkanSDK:
    """Main SDK client for interacting with cryptocurrency exchanges."""

    @catch_exception
    def __init__(self):
        self._orderbook_manager = None
        self._trades_manager = None
        self._running = True
        logger.info("Initialized Bjarkan SDK")

    @catch_exception
    async def set_config(self, *, type: str, **config_params) -> Dict:
        """Unified configuration method for both orderbook and trades.

        Args:
            type: The type of configuration ('orderbook' or 'trades')
            **config_params: Configuration parameters specific to the type

        Returns:
            Dict with status and message

        Examples:
            >>> await sdk.set_config(
            ...     type="orderbook",
            ...     aggregated=True,
            ...     exchanges=["binance", "okx"],
            ...     symbols=["BTC/USDT"],
            ...     depth=10
            ... )
        """
        if not isinstance(type, str):
            raise BjarkanError(f"Config type must be a string, got {type.__class__.__name__}")

        type = type.lower()
        if type not in ['orderbook', 'trades']:
            raise BjarkanError(
                f"Invalid config type: '{type}'. Must be 'orderbook' or 'trades'."
                "\nExample usage:"
                "\n  await sdk.set_config("
                "\n      type='orderbook',"
                "\n      aggregated=True,"
                "\n      exchanges=['binance', 'okx'],"
                "\n      symbols=['BTC/USDT'],"
                "\n      depth=10"
                "\n  )"
            )

        try:
            if type == 'orderbook':
                config = OrderbookConfig(**config_params)
                self._orderbook_manager = OrderbookManager(config)
                return {"status": "success", "message": "Orderbook configuration set"}
            else:  # trades
                config = TradesConfig(**config_params)
                self._trades_manager = TradesManager(config)
                return {"status": "success", "message": "Trades configuration set"}
        except ValueError as e:
            raise BjarkanError(str(e))
        except Exception as e:
            if "exchanges" in str(e):
                raise BjarkanError(
                    f"Invalid exchanges configuration: {str(e)}"
                    "\nMake sure exchanges is a non-empty list of strings."
                )
            elif "symbols" in str(e):
                raise BjarkanError(
                    f"Invalid symbols configuration: {str(e)}"
                    "\nMake sure symbols is a non-empty list of valid trading pairs."
                )
            elif "depth" in str(e):
                raise BjarkanError(
                    f"Invalid depth configuration: {str(e)}"
                    "\nDepth must be a positive integer."
                )
            else:
                raise BjarkanError(f"Failed to set {type} config: {str(e)}")

    @catch_exception
    async def start_stream(self, stream_type: str, callback: Optional[Callable] = None) -> Dict:
        """Unified method to start either orderbook or trades stream."""
        if stream_type not in ['orderbook', 'trades']:
            raise BjarkanError(f"Invalid stream type: {stream_type}. Must be 'orderbook' or 'trades'")

        try:
            if stream_type == 'orderbook':
                if not self._orderbook_manager:
                    raise BjarkanError("Orderbook not configured")
                if callback:
                    self._orderbook_manager.add_callback(callback)
                await self._orderbook_manager.start()
                return {"status": "success", "message": "Orderbook stream started"}
            else:  # trades
                if not self._trades_manager:
                    raise BjarkanError("Trades not configured")
                if callback:
                    self._trades_manager.add_callback(callback)
                await self._trades_manager.start()
                return {"status": "success", "message": "Trades stream started"}
        except Exception as e:
            raise BjarkanError(f"Failed to start {stream_type} stream: {str(e)}")

    @catch_exception
    async def stop_stream(self, stream_type: str) -> Dict:
        """Unified method to stop either orderbook or trades stream."""
        if stream_type not in ['orderbook', 'trades']:
            raise BjarkanError(f"Invalid stream type: {stream_type}. Must be 'orderbook' or 'trades'")

        try:
            if stream_type == 'orderbook':
                if self._orderbook_manager:
                    await self._orderbook_manager.close()
                    return {"status": "success", "message": "Orderbook stream stopped"}
            else:  # trades
                if self._trades_manager:
                    await self._trades_manager.close()
                    return {"status": "success", "message": "Trades stream stopped"}
            return {"status": "success", "message": f"{stream_type} stream was not running"}
        except Exception as e:
            raise BjarkanError(f"Failed to stop {stream_type} stream: {str(e)}")

    @catch_exception
    async def get_latest_data(self, data_type: str) -> Dict:
        """Unified method to get latest data from either orderbook or trades."""
        if data_type not in ['orderbook', 'trades']:
            raise BjarkanError(f"Invalid data type: {data_type}. Must be 'orderbook' or 'trades'")

        try:
            if data_type == 'orderbook':
                if not self._orderbook_manager:
                    raise BjarkanError("Orderbook not configured")
                return await self._orderbook_manager.get_latest_orderbooks()
            else:  # trades
                if not self._trades_manager:
                    raise BjarkanError("Trades not configured")
                return await self._trades_manager.get_latest_trades()
        except Exception as e:
            raise BjarkanError(f"Failed to get latest {data_type} data: {str(e)}")

    @catch_exception
    async def execute_order(self, order: OrderConfig, api_configs: List[APIConfig]) -> Dict:
        """Execute an order using smart order routing with provided API configurations."""
        if not self._orderbook_manager:
            raise BjarkanError("Orderbook must be configured before executing orders")

        try:
            # Get latest orderbook data for execution
            orderbook = await self.get_latest_data('orderbook')

            # Create temporary executor for this order
            executor = OrderExecutor(self._orderbook_manager.orderbook_config, api_configs)

            # Execute the order
            await executor.update_orderbook(orderbook)
            result = await executor.execute_order(order)

            # Clean up
            await executor.close()

            return result

        except Exception as e:
            if isinstance(e, ccxt.AuthenticationError):
                raise BjarkanError("Invalid API credentials provided")
            elif isinstance(e, ccxt.InsufficientFunds):
                raise BjarkanError("Insufficient funds for order execution")
            else:
                raise BjarkanError(f"Failed to execute order: {str(e)}")

    @catch_exception
    async def close(self):
        """Clean up resources and close connections."""
        self._running = False
        tasks = []

        if self._orderbook_manager:
            tasks.append(self._orderbook_manager.close())
        if self._trades_manager:
            tasks.append(self._trades_manager.close())

        await asyncio.gather(*tasks, return_exceptions=True)
        logger.info("SDK closed")
