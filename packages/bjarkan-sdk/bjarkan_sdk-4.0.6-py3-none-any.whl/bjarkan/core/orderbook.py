import asyncio
import time
from typing import Dict, List, Tuple
import ccxt.pro as ccxt
from bjarkan.models import OrderbookConfig
from bjarkan.utils.logger import logger, catch_exception
from bjarkan.config import EXCHANGES


class OrderbookManager:
    @catch_exception
    def __init__(self, orderbook_config: OrderbookConfig):
        self.orderbook_config = orderbook_config
        self.symbols = orderbook_config.symbols
        self.depth = min(orderbook_config.depth, 50)
        self.aggregated = orderbook_config.aggregated
        self.exchanges = self._initialize_exchanges()
        self.fees = self._initialize_fees()
        self.orderbooks = {ex: {symbol: None for symbol in self.symbols} for ex in self.exchanges}
        self.running = True
        self.lock = asyncio.Lock()
        self.update_event = asyncio.Event()
        self.weighting = orderbook_config.weighting
        self._callbacks = []

    @catch_exception
    def _initialize_exchanges(self) -> Dict[str, ccxt.Exchange]:
        exchanges = {}
        for exchange_id in self.orderbook_config.exchanges:
            exchange_class = getattr(ccxt, exchange_id)
            instance = exchange_class({'enableRateLimit': True})
            is_sandbox = self.orderbook_config.sandbox_mode.get(exchange_id, False)
            instance.set_sandbox_mode(is_sandbox)
            exchanges[exchange_id] = instance
        return exchanges

    @catch_exception
    def _initialize_fees(self) -> Dict[str, Dict[str, float]]:
        if not self.orderbook_config.fees_bps:
            return {exchange: {symbol: 1 for symbol in self.symbols} for exchange in self.exchanges}

        fees = {}
        for exchange, fee_info in self.orderbook_config.fees_bps.items():
            if isinstance(fee_info, dict):
                fees[exchange] = {symbol: 1 + fee / 10000 for symbol, fee in fee_info.items()}
            else:
                fees[exchange] = {symbol: 1 + fee_info / 10000 for symbol in self.symbols}
        return fees

    @catch_exception
    def get_exchange_depth(self, exchange: str) -> int:
        available_depths = EXCHANGES[exchange]['available_depth']
        if isinstance(available_depths, range):
            return min(self.depth, max(available_depths))
        suitable_depths = [d for d in available_depths if d >= self.depth]
        return min(suitable_depths) if suitable_depths else max(available_depths)

    @catch_exception
    def apply_fees(self, exchange: str, symbol: str, bids: List[Tuple], asks: List[Tuple]) -> Tuple[
        List[Tuple], List[Tuple]]:
        fee = self.fees.get(exchange, {}).get(symbol, 1)
        if fee != 1:
            bids = [(round(float(price) * (1 / fee), 8), amount, exchange) for price, amount, exchange in bids]
            asks = [(round(float(price) * fee, 8), amount, exchange) for price, amount, exchange in asks]
        return bids, asks

    @catch_exception
    async def collect_orderbook(self, exchange_name: str, symbol: str):
        exchange = self.exchanges[exchange_name]
        exchange_depth = self.get_exchange_depth(exchange_name)

        while self.running:
            try:
                # Get raw data
                orderbook = await exchange.watchOrderBook(symbol, exchange_depth)

                # Process orders and add exchange name
                bids = [(float(price), float(amount), exchange_name) for price, amount in
                        orderbook['bids'][:self.depth]]
                asks = [(float(price), float(amount), exchange_name) for price, amount in
                        orderbook['asks'][:self.depth]]

                # Apply fees
                bids, asks = self.apply_fees(exchange_name, symbol, bids, asks)

                processed_orderbook = {
                    'timestamp': int(time.time() * 1000),
                    'exchange_timestamp': orderbook.get('timestamp'),
                    'symbol': symbol,
                    'bids': bids,
                    'asks': asks
                }

                async with self.lock:
                    self.orderbooks[exchange_name][symbol] = processed_orderbook

                    # Get aggregated data if needed
                    if self.aggregated:
                        current_books = {
                            ex: {symbol: ob.copy() for symbol, ob in symbol_obs.items() if ob}
                            for ex, symbol_obs in self.orderbooks.items()
                        }
                        aggregated_books = self.aggregate_orderbooks(current_books)
                        # Send aggregated data to callbacks
                        book_to_send = aggregated_books.get(symbol)
                    else:
                        # Send individual exchange data
                        book_to_send = processed_orderbook

                # Execute callbacks with appropriate data
                if book_to_send:
                    for callback in self._callbacks:
                        try:
                            await callback(book_to_send)
                        except Exception as e:
                            logger.error(f"Error in orderbook callback: {str(e)}")

                self.update_event.set()

            except asyncio.CancelledError:
                break
            except Exception as e:
                if self.running:
                    logger.error(f"Error collecting orderbook from {exchange_name}.{symbol}: {str(e)}")
                await asyncio.sleep(5)

    @staticmethod
    @catch_exception
    def calculate_vwap(orders: List[Tuple], target_amount: float) -> List[Tuple]:
        vwap_orders = []
        total_amount = 0
        total_value = 0
        exchange = orders[0][2] if orders else None
        original_target = target_amount

        for price, amount, _ in orders:
            if total_amount + amount >= target_amount:
                needed_amount = target_amount - total_amount
                total_value += price * needed_amount
                total_amount += needed_amount
                vwap_price = total_value / total_amount
                vwap_orders.append((vwap_price, target_amount, exchange))

                total_amount = amount - needed_amount
                total_value = price * total_amount
                target_amount = original_target
            else:
                total_value += price * amount
                total_amount += amount

            if total_amount >= target_amount:
                vwap_price = total_value / total_amount
                vwap_orders.append((vwap_price, target_amount, exchange))
                total_amount = 0
                total_value = 0
                target_amount = original_target

        return vwap_orders

    @catch_exception
    def apply_vwap(self, orderbooks: Dict) -> Dict:
        if not self.weighting:
            return orderbooks

        vwap_orderbooks = {}
        for exchange, exchange_orderbooks in orderbooks.items():
            vwap_orderbooks[exchange] = {}
            for symbol, book in exchange_orderbooks.items():
                vwap_orderbooks[exchange][symbol] = book.copy()
                if symbol in self.weighting:
                    currency, target_amount = next(iter(self.weighting[symbol].items()))
                    base, quote = symbol.split('/')
                    if currency == base:
                        vwap_orderbooks[exchange][symbol]['bids'] = self.calculate_vwap(book['bids'], target_amount)
                        vwap_orderbooks[exchange][symbol]['asks'] = self.calculate_vwap(book['asks'], target_amount)
                    elif currency == quote:
                        if book['bids']:
                            quote_target = target_amount / book['bids'][0][0]
                            vwap_orderbooks[exchange][symbol]['bids'] = self.calculate_vwap(book['bids'], quote_target)
                            vwap_orderbooks[exchange][symbol]['asks'] = self.calculate_vwap(book['asks'], quote_target)
                        else:
                            vwap_orderbooks[exchange][symbol]['bids'] = []
                            vwap_orderbooks[exchange][symbol]['asks'] = []

        return vwap_orderbooks

    @catch_exception
    def aggregate_orderbooks(self, orderbooks: Dict) -> Dict:
        aggregated = {}
        for symbol in self.symbols:
            all_bids = []
            all_asks = []
            valid_exchange_timestamps = []

            for exchange, exchange_obs in orderbooks.items():
                ob = exchange_obs.get(symbol)
                if ob:
                    all_bids.extend(ob['bids'])
                    all_asks.extend(ob['asks'])
                    if ob['exchange_timestamp'] is not None:
                        valid_exchange_timestamps.append(ob['exchange_timestamp'])

            if all_bids and all_asks:
                aggregated[symbol] = {
                    'timestamp': int(time.time() * 1000),
                    'exchange_timestamp': max(valid_exchange_timestamps) if valid_exchange_timestamps else None,
                    'symbol': symbol,
                    'bids': sorted(all_bids, key=lambda x: float(x[0]), reverse=True)[:self.depth],
                    'asks': sorted(all_asks, key=lambda x: float(x[0]))[:self.depth]
                }

        return aggregated

    @catch_exception
    async def get_latest_orderbooks(self) -> Dict:
        async with self.lock:
            # Get current orderbooks with proper copying
            raw_orderbooks = {
                ex: {symbol: ob.copy() for symbol, ob in symbol_obs.items() if ob}
                for ex, symbol_obs in self.orderbooks.items()
            }

            # Apply VWAP if configured
            if self.weighting:
                vwap_orderbooks = self.apply_vwap(raw_orderbooks)
                final_orderbooks = self.aggregate_orderbooks(vwap_orderbooks) if self.aggregated else vwap_orderbooks
            else:
                final_orderbooks = self.aggregate_orderbooks(raw_orderbooks) if self.aggregated else raw_orderbooks

            return final_orderbooks

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
            self.collect_orderbook(exchange, symbol)
            for exchange in self.exchanges
            for symbol in self.symbols
        ]
        await asyncio.gather(*tasks, return_exceptions=True)

    @catch_exception
    async def close(self):
        self.running = False
        await asyncio.gather(*[exchange.close() for exchange in self.exchanges.values()], return_exceptions=True)
        self._callbacks.clear()
