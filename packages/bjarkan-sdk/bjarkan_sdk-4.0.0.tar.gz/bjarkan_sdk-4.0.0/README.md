# Bjarkan SDK

A powerful cryptocurrency trading SDK with smart order routing capabilities and real-time market data aggregation.

## Features

- Real-time market data aggregation from multiple exchanges
- Fee-aware orderbook processing
- VWAP calculations
- Smart order routing and execution
- Trade monitoring and filtering
- Unified API interface for all exchanges
- Comprehensive error handling
- Sandbox mode support

## Installation

```bash
pip install bjarkan-sdk
```

## Quick Start

```python
import asyncio
from bjarkan import BjarkanSDK, OrderConfig, APIConfig

async def main():
    # Initialize SDK
    sdk = BjarkanSDK()
    
    # Configure orderbook data
    await sdk.set_config(
        type="orderbook",
        aggregated=True,
        exchanges=["binance", "okx"],
        symbols=["BTC/USDT"],
        depth=10,
        fees_bps={
            "binance": 10,
            "okx": 8
        }
    )
    
    # Start the orderbook stream
    await sdk.start_stream(stream_type="orderbook")
    
    # Get real-time orderbook data
    orderbook = await sdk.get_latest_data("orderbook")
    print(orderbook)
    
    # Execute a trade (requires API keys)
    api_configs = [
        APIConfig(
            exchange="binance",
            api_key="your_api_key",
            secret="your_secret"
        )
    ]
    
    order = OrderConfig(
        side="buy",
        type="limit",
        time_in_force="gtc",
        amount=0.01,
        price=50000.0
    )
    
    result = await sdk.execute_order(order, api_configs)
    print(result)
    
    # Cleanup
    await sdk.close()

if __name__ == "__main__":
    asyncio.run(main())
```

## Advanced Usage

For more advanced features like VWAP calculations and trade monitoring, check the examples directory.

### Setting Up Configurations

```python
# Orderbook configuration
await sdk.set_config(
    type="orderbook",
    aggregated=True,
    exchanges=["binance", "okx", "kraken"],
    symbols=["BTC/USDT", "ETH/USDT"],
    depth=20,
    fees_bps={
        "binance": 10,
        "okx": {"BTC/USDT": 8, "ETH/USDT": 8},
        "kraken": 10
    },
    weighting={  # Enable VWAP
        "BTC/USDT": {"USDT": 20000},
        "ETH/USDT": {"USDT": 10000}
    }
)

# Trades configuration
await sdk.set_config(
    type="trades",
    exchanges=["binance", "okx", "kraken"],
    symbols=["BTC/USDT", "ETH/USDT"],
    size={  # Minimum trade size filter
        "BTC/USDT": {"BTC": 0.001},
        "ETH/USDT": {"ETH": 0.01}
    }
)
```

### Managing Data Streams

```python
# Start streams
await sdk.start_stream("orderbook")
await sdk.start_stream("trades")

# Get latest data
orderbook_data = await sdk.get_latest_data("orderbook")
trades_data = await sdk.get_latest_data("trades")

# Stop streams
await sdk.stop_stream("orderbook")
await sdk.stop_stream("trades")
```

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/bjarkan-sdk.git
cd bjarkan-sdk
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
./run.sh env_setup.sh --all
```

## Testing

Run the test suite:
```bash
pytest tests/
```

Run with coverage:
```bash
pytest tests/ --cov=bjarkan --cov-report=term-missing
```

## Deployment

1. Update version number:
```bash
python bump_version.py patch  # or minor/major
```

2. Deploy to PyPI:
```bash
./deploy.sh
```

## Environment Variables

Create a `.env` file in your project root:

```env
# API Keys (for trading)
BINANCE_API_KEY=your_api_key
BINANCE_SECRET=your_secret
OKX_API_KEY=your_api_key
OKX_SECRET=your_secret
OKX_PASSWORD=your_password

# Logging (optional)
BETTERSTACK_TOKEN=your_token
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.