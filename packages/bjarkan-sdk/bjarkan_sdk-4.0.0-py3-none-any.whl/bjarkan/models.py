from pydantic import BaseModel, field_validator, model_validator
from typing import List, Dict, Union, Optional


class OrderbookConfig(BaseModel):
    aggregated: bool = False
    exchanges: List[str]
    sandbox_mode: Dict[str, bool] = {}
    symbols: List[str]
    depth: int
    fees_bps: Optional[Dict[str, Union[float, Dict[str, float]]]] = None
    weighting: Optional[Dict[str, Dict[str, float]]] = None  # If present, VWAP is enabled

    @field_validator('exchanges')
    @classmethod
    def validate_exchanges(cls, v: List[str]) -> List[str]:
        return [exchange.lower() for exchange in v]

    @field_validator('symbols')
    @classmethod
    def validate_symbols(cls, v: List[str]) -> List[str]:
        return [symbol.upper() for symbol in v]

    @field_validator('depth')
    @classmethod
    def validate_depth(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("Depth must be a positive integer")
        return v

    @model_validator(mode='after')
    def validate_weighting_config(self):
        if self.weighting:
            for symbol, weight in self.weighting.items():
                if symbol not in self.symbols:
                    raise ValueError(f"Weighting specified for symbol {symbol} which is not in the symbols list")
                if len(weight) != 1:
                    raise ValueError(f"Weighting for {symbol} should have exactly one currency-amount pair")
                currency, amount = next(iter(weight.items()))
                if currency not in symbol.split('/'):
                    raise ValueError(f"Weighting currency {currency} not found in symbol {symbol}")
                if amount <= 0:
                    raise ValueError(f"Weighting amount for {symbol} must be positive")
        return self


class TradesConfig(BaseModel):
    exchanges: List[str]
    sandbox_mode: Dict[str, bool] = {}
    symbols: List[str]
    fees_bps: Optional[Dict[str, Union[float, Dict[str, float]]]] = None
    size: Optional[Dict[str, Dict[str, float]]] = None

    @field_validator('exchanges')
    @classmethod
    def validate_exchanges(cls, v: List[str]) -> List[str]:
        return [exchange.lower() for exchange in v]

    @field_validator('symbols')
    @classmethod
    def validate_symbols(cls, v: List[str]) -> List[str]:
        return [symbol.upper() for symbol in v]

    @model_validator(mode='after')
    def validate_size_config(self):
        if self.size:
            for symbol, size_info in self.size.items():
                if symbol not in self.symbols:
                    raise ValueError(f"Size specified for symbol {symbol} which is not in the symbols list")
                if len(size_info) != 1:
                    raise ValueError(f"Size for {symbol} should have exactly one currency-amount pair")
                currency, amount = next(iter(size_info.items()))
                if currency not in symbol.split('/'):
                    raise ValueError(f"Size currency {currency} not found in symbol {symbol}")
                if amount <= 0:
                    raise ValueError(f"Size amount for {symbol} must be positive")
        return self


class APIConfig(BaseModel):
    """API configuration for exchange access."""
    exchange: str
    api_key: str
    secret: str
    password: Optional[str] = None

    @field_validator('exchange')
    @classmethod
    def validate_exchange(cls, v: str) -> str:
        return v.lower()

    @field_validator('api_key', 'secret')
    @classmethod
    def validate_credentials(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("API credentials cannot be empty")
        return v.strip()


class OrderConfig(BaseModel):
    """Configuration for order execution."""
    side: str
    type: str
    time_in_force: str
    amount: float
    price: Optional[float] = None

    @model_validator(mode='after')
    def validate_order_config(self):
        if self.side.lower() not in ['buy', 'sell']:
            raise ValueError("Side must be either 'buy' or 'sell'")

        if self.type.lower() not in ['market', 'limit']:
            raise ValueError("Type must be either 'market' or 'limit'")

        valid_tif = ['gtc', 'fok', 'ioc']
        if self.time_in_force.lower() not in valid_tif:
            raise ValueError(f"Time in force must be one of {', '.join(valid_tif)}")

        if self.type.lower() == 'limit' and self.price is None:
            raise ValueError("Price must be specified for limit orders")

        if self.type.lower() == 'market' and self.time_in_force.lower() != 'ioc':
            raise ValueError("Time in force must be 'IOC' for market orders")

        return self

    @field_validator('amount')
    @classmethod
    def validate_amount(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Amount must be greater than 0")
        return v

    @field_validator('side', 'type', 'time_in_force')
    @classmethod
    def normalize_string_fields(cls, v: str) -> str:
        return v.lower() if v else v
