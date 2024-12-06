import asyncio
from typing import Dict, List
import ccxt.pro as ccxt
import time
from bjarkan.models import OrderbookConfig, OrderConfig, APIConfig
from bjarkan.utils.logger import logger, catch_exception
from bjarkan.exceptions import BjarkanError


class OrderExecutor:
    @catch_exception
    def __init__(self, orderbook_config: OrderbookConfig, api_configs: List[APIConfig]):
        if not orderbook_config.aggregated or len(orderbook_config.symbols) != 1:
            raise ValueError("OrderExecutor requires aggregated data and exactly one symbol in orderbook_config")

        self.orderbook_config = orderbook_config
        self.api_configs = {config.exchange: config for config in api_configs}
        self.exchanges = {}
        self.symbol = orderbook_config.symbols[0]
        self.latest_orderbook = None

        # Validate and initialize exchanges
        self._initialize_exchanges()

    @catch_exception
    def _initialize_exchanges(self):
        """Initialize exchange connections with error handling."""
        for exchange_id in self.orderbook_config.exchanges:
            if exchange_id not in self.api_configs:
                continue  # Skip exchanges without API configs

            config = self.api_configs[exchange_id]
            exchange_class = getattr(ccxt, exchange_id)

            try:
                exchange = exchange_class({
                    'apiKey': config.api_key,
                    'secret': config.secret,
                    'password': config.password,
                    'enableRateLimit': True,
                })

                # Test authentication
                exchange.check_required_credentials()

                is_sandbox = self.orderbook_config.sandbox_mode.get(exchange_id, False)
                exchange.set_sandbox_mode(is_sandbox)

                self.exchanges[exchange_id] = exchange

            except ccxt.AuthenticationError as e:
                logger.error(f"Authentication failed for {exchange_id}: {str(e)}")
                raise BjarkanError(f"Invalid API credentials for {exchange_id}")
            except Exception as e:
                logger.error(f"Failed to initialize {exchange_id}: {str(e)}")
                raise BjarkanError(f"Failed to initialize {exchange_id}: {str(e)}")

        if not self.exchanges:
            raise BjarkanError("No exchanges could be initialized with provided API configurations")

    @catch_exception
    async def update_orderbook(self, orderbook: Dict):
        """Update the latest orderbook data."""
        if self.symbol not in orderbook:
            raise BjarkanError(f"No orderbook data available for symbol {self.symbol}")
        self.latest_orderbook = orderbook[self.symbol]

    @catch_exception
    async def execute_order(self, order: OrderConfig) -> Dict:
        """Execute an order across available exchanges."""
        if not self.latest_orderbook:
            raise BjarkanError("No orderbook data available")

        if not self.exchanges:
            raise BjarkanError("No exchanges initialized with valid API keys")

        execution_plan = self._create_execution_plan(order)
        if not execution_plan:
            raise BjarkanError("Could not create valid execution plan with available liquidity")

        execution_results = []
        remaining_amount = order.amount
        total_filled_amount = 0
        start_time = time.time()

        for exchange_id, amount, price in execution_plan:
            if exchange_id not in self.exchanges:
                logger.warning(f"Skipping {exchange_id} - no valid API configuration")
                continue

            try:
                exchange = self.exchanges[exchange_id]
                params = {'timeInForce': order.time_in_force} if order.type == 'limit' else {}

                executed_order = await exchange.createOrder(
                    self.symbol,
                    order.type,
                    order.side,
                    amount,
                    price if order.type == 'limit' else None,
                    params
                )

                filled_amount = float(executed_order.get('filled', 0) or 0)
                total_filled_amount += filled_amount
                remaining_amount = max(0, remaining_amount - filled_amount)

                execution_results.append({
                    "exchange": exchange_id,
                    "order": executed_order,
                    "status": "success",
                    "planned_amount": amount,
                    "filled_amount": filled_amount,
                    "planned_price": price,
                    "actual_price": executed_order.get('price'),
                })

            except ccxt.InsufficientFunds:
                logger.error(f"Insufficient funds on {exchange_id}")
                execution_results.append({
                    "exchange": exchange_id,
                    "error": "Insufficient funds",
                    "status": "failed",
                    "planned_amount": amount,
                    "planned_price": price
                })
            except Exception as e:
                logger.error(f"Error executing order on {exchange_id}: {str(e)}")
                execution_results.append({
                    "exchange": exchange_id,
                    "error": str(e),
                    "status": "failed",
                    "planned_amount": amount,
                    "planned_price": price
                })

        total_time = time.time() - start_time

        return {
            "status": "completed" if remaining_amount <= 1e-8 else "partially_filled",
            "original_amount": order.amount,
            "filled_amount": total_filled_amount,
            "remaining_amount": remaining_amount,
            "execution_results": execution_results,
            "execution_plan": execution_plan,
            "total_execution_time": round(total_time * 1000, 2),  # milliseconds
        }

    @catch_exception
    def _create_execution_plan(self, order: OrderConfig) -> List[tuple]:
        """Create an execution plan based on available liquidity."""
        execution_plan = []
        remaining_amount = order.amount
        book_side = self.latest_orderbook['bids'] if order.side == 'sell' else self.latest_orderbook['asks']

        for price, size, exchange in book_side:
            if remaining_amount <= 0:
                break
            if exchange in self.exchanges:  # Only include exchanges we have API keys for
                executable_amount = min(remaining_amount, size)
                execution_plan.append((exchange, executable_amount, price))
                remaining_amount -= executable_amount

        return execution_plan

    @catch_exception
    async def close(self):
        """Close all exchange connections."""
        close_tasks = []
        for exchange in self.exchanges.values():
            if hasattr(exchange, 'close'):
                close_tasks.append(exchange.close())

        if close_tasks:
            await asyncio.gather(*close_tasks, return_exceptions=True)
