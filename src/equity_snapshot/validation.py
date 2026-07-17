"""Validation helpers for equity snapshot inputs."""

import re

from equity_snapshot.exceptions import InvalidTickerError


TICKER_PATTERN = re.compile(r"^[A-Z0-9][A-Z0-9.\-]{0,14}$")


def normalize_ticker(ticker: str) -> str:
    """Normalize and validate a stock ticker."""

    if not isinstance(ticker, str):
        raise InvalidTickerError("Ticker must be a string.")

    normalized = ticker.strip().upper()

    if not normalized:
        raise InvalidTickerError("Ticker cannot be empty.")

    if not TICKER_PATTERN.fullmatch(normalized):
        raise InvalidTickerError("Ticker may contain only letters, numbers, periods, and hyphens.")

    return normalized
