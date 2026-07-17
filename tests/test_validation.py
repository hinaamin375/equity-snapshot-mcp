import pytest

from equity_snapshot.exceptions import InvalidTickerError
from equity_snapshot.validation import normalize_ticker


@pytest.mark.parametrize(
    ("input_value", "expected"),
    [
        ("aapl", "AAPL"),
        (" msft ", "MSFT"),
        ("brk-b", "BRK-B"),
        ("7203.t", "7203.T"),
    ],
)
def test_normalize_valid_ticker(input_value: str, expected: str) -> None:
    assert normalize_ticker(input_value) == expected


@pytest.mark.parametrize(
    "input_value",
    [
        "",
        "   ",
        "AAPL!",
        "DROP TABLE",
        "$AAPL",
    ],
)
def test_reject_invalid_ticker(input_value: str) -> None:
    with pytest.raises(InvalidTickerError):
        normalize_ticker(input_value)
