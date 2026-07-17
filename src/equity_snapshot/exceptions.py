"""Custom exceptions for equity snapshot operations."""


class StockResearchError(Exception):
    """Base exception for the project."""


class InvalidTickerError(StockResearchError):
    """Raised when a ticker has an invalid format."""


class TickerNotFoundError(StockResearchError):
    """Raised when the provider cannot find the ticker."""


class ProviderError(StockResearchError):
    """Raised when the market-data provider fails."""
