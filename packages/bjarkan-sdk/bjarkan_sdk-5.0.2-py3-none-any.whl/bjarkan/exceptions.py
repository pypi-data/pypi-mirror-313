class BjarkanError(Exception):
    """Base exception class for Bjarkan SDK errors."""
    pass


class BjarkanAuthenticationError(BjarkanError):
    """Raised when API authentication fails."""
    pass


class BjarkanInsufficientFundsError(BjarkanError):
    """Raised when there are insufficient funds for order execution."""
    pass


class BjarkanOrderExecutionError(BjarkanError):
    """Raised when order execution fails."""
    pass
