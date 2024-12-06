import asyncio
import time
from typing import Dict, List
import ccxt.pro as ccxt
from bjarkan.models import TradesConfig
from bjarkan.utils.logger import logger, catch_exception


class TradesManager:
    @catch_exception
    def __init__(self, trades_config: TradesConfig):
        self.trades_config = trades_config
        self.symbols = trades_config.symbols
        self.exchanges = self._initialize_exchanges()
        self.fees = self._initialize_fees()
        self.size_filters = trades_config.size or {}
        self.trades = {ex: {symbol: [] for symbol in self.symbols} for ex in self.exchanges}
        self.running = True
        self.lock = asyncio.Lock()
        self.update_event = asyncio.Event()
        self._callbacks = []

    @catch_exception
    def _initialize_exchanges(self) -> Dict[str, ccxt.Exchange]:
        exchanges = {}
        for exchange_id in self.trades_config.exchanges:
            exchange_class = getattr(ccxt, exchange_id)
            instance = exchange_class({'enableRateLimit': True})
            is_sandbox = self.trades_config.sandbox_mode.get(exchange_id, False)
            instance.set_sandbox_mode(is_sandbox)
            exchanges[exchange_id] = instance
        return exchanges

    @catch_exception
    def _initialize_fees(self) -> Dict[str, Dict[str, float]]:
        if not self.trades_config.fees_bps:
            return {exchange: {symbol: 0 for symbol in self.symbols} for exchange in self.exchanges}

        fees = {}
        for exchange, fee_info in self.trades_config.fees_bps.items():
            if isinstance(fee_info, dict):
                fees[exchange] = {symbol: fee / 10000 for symbol, fee in fee_info.items()}
            else:
                fees[exchange] = {symbol: fee_info / 10000 for symbol in self.symbols}
        return fees

    @catch_exception
    def apply_fees(self, exchange: str, symbol: str, price: float, amount: float) -> tuple:
        fee = self.fees.get(exchange, {}).get(symbol, 0)
        if fee != 0:
            price = round(price * (1 + fee), 8)
        return price, amount

    @catch_exception
    def filter_by_size(self, symbol: str, price: float, amount: float) -> bool:
        if symbol not in self.size_filters:
            return True

        filter_info = self.size_filters[symbol]
        base, quote = symbol.split('/')

        if base in filter_info:
            return amount >= filter_info[base]
        elif quote in filter_info:
            return price * amount >= filter_info[quote]

        return True

    @catch_exception
    async def collect_trades(self, exchange_name: str, symbol: str):
        exchange = self.exchanges[exchange_name]

        while self.running:
            try:
                trades = await exchange.watch_trades(symbol)

                for trade in trades:
                    price, amount = self.apply_fees(exchange_name, symbol, trade['price'], trade['amount'])

                    if self.filter_by_size(symbol, price, amount):
                        processed_trade = {
                            'id': trade['id'],
                            'timestamp': int(time.time() * 1000),
                            'exchange_timestamp': trade['timestamp'],
                            'price': price,
                            'amount': amount,
                            'side': trade['side']
                        }

                        async with self.lock:
                            self.trades[exchange_name][symbol].append(processed_trade)

                        self.update_event.set()

                        for callback in self._callbacks:
                            try:
                                await callback(processed_trade)
                            except Exception as e:
                                logger.error(f"Error in trade callback: {str(e)}")

            except asyncio.CancelledError:
                break
            except Exception as e:
                if self.running:
                    logger.error(f"Error collecting trades from {exchange_name}.{symbol}: {str(e)}")
                await asyncio.sleep(5)

    @catch_exception
    async def get_latest_trades(self) -> Dict[str, Dict[str, List]]:
        async with self.lock:
            latest_trades = {
                ex: {symbol: trades.copy() for symbol, trades in symbol_trades.items()}
                for ex, symbol_trades in self.trades.items()
            }

            for ex in self.trades:
                for symbol in self.trades[ex]:
                    self.trades[ex][symbol].clear()

            return latest_trades

    @catch_exception
    def add_callback(self, callback):
        self._callbacks.append(callback)

    @catch_exception
    def remove_callback(self, callback):
        if callback in self._callbacks:
            self._callbacks.remove(callback)

    @catch_exception
    async def start(self):
        tasks = [
            self.collect_trades(exchange, symbol)
            for exchange in self.exchanges
            for symbol in self.symbols
        ]
        await asyncio.gather(*tasks, return_exceptions=True)

    @catch_exception
    async def close(self):
        self.running = False
        await asyncio.gather(*[exchange.close() for exchange in self.exchanges.values()], return_exceptions=True)
        self._callbacks.clear()