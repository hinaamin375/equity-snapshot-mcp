from unittest.mock import MagicMock, patch

from equity_snapshot.provider import (
    get_company_profile,
    get_financial_snapshot,
)


MOCK_INFO = {
    "symbol": "TEST",
    "longName": "Test Corporation",
    "exchange": "NASDAQ",
    "sector": "Technology",
    "industry": "Software",
    "currency": "USD",
    "marketCap": 1_000_000_000,
    "longBusinessSummary": "A test company.",
    "totalRevenue": 500_000_000,
    "revenueGrowth": 0.12,
    "netIncomeToCommon": 80_000_000,
    "profitMargins": 0.16,
    "freeCashflow": 70_000_000,
    "totalCash": 120_000_000,
    "totalDebt": 40_000_000,
    "trailingPE": 22.5,
}


@patch("equity_snapshot.provider.yf.Ticker")
def test_get_company_profile(mock_ticker: MagicMock) -> None:
    mock_ticker.return_value.info = MOCK_INFO

    result = get_company_profile("test")

    assert result.ticker == "TEST"
    assert result.company_name == "Test Corporation"
    assert result.sector == "Technology"
    assert result.market_cap == 1_000_000_000


@patch("equity_snapshot.provider.yf.Ticker")
def test_get_financial_snapshot(mock_ticker: MagicMock) -> None:
    mock_ticker.return_value.info = MOCK_INFO

    result = get_financial_snapshot("test")

    assert result.revenue == 500_000_000
    assert result.revenue_growth == 0.12
    assert result.profit_margin == 0.16
    assert result.trailing_pe == 22.5
    assert result.warnings == []


@patch("equity_snapshot.provider.yf.Ticker")
def test_missing_values_create_warning(mock_ticker: MagicMock) -> None:
    mock_ticker.return_value.info = {
        "symbol": "TEST",
        "longName": "Test Corporation",
        "currency": "USD",
    }

    result = get_financial_snapshot("TEST")

    assert result.revenue is None
    assert result.trailing_pe is None
    assert result.warnings
    assert "revenue" in result.warnings[0]
