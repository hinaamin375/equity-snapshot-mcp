from unittest.mock import patch

import pytest

from equity_snapshot.models import DataSource, FinancialSnapshot
from equity_snapshot.services import (
    compare_stocks,
    get_research_summary,
)


def make_snapshot(
    ticker: str,
    revenue_growth: float | None,
    profit_margin: float | None,
    free_cash_flow: float | None,
    cash: float | None,
    total_debt: float | None,
    trailing_pe: float | None,
) -> FinancialSnapshot:
    return FinancialSnapshot(
        ticker=ticker,
        company_name=f"{ticker} Company",
        currency="USD",
        revenue=1_000_000,
        revenue_growth=revenue_growth,
        net_income=100_000,
        profit_margin=profit_margin,
        free_cash_flow=free_cash_flow,
        cash=cash,
        total_debt=total_debt,
        trailing_pe=trailing_pe,
        source=DataSource(provider="Test provider"),
    )


@patch("equity_snapshot.services.get_financial_snapshot")
def test_compare_stocks(mock_snapshot) -> None:
    mock_snapshot.side_effect = [
        make_snapshot(
            ticker="AAA",
            revenue_growth=0.20,
            profit_margin=0.15,
            free_cash_flow=200,
            cash=500,
            total_debt=100,
            trailing_pe=25,
        ),
        make_snapshot(
            ticker="BBB",
            revenue_growth=0.10,
            profit_margin=0.25,
            free_cash_flow=300,
            cash=100,
            total_debt=400,
            trailing_pe=18,
        ),
    ]

    result = compare_stocks(["AAA", "BBB"])

    assert result.tickers == ["AAA", "BBB"]
    assert len(result.companies) == 2
    assert any(
        "AAA has the highest revenue growth" in observation for observation in result.observations
    )
    assert any(
        "BBB has the lowest trailing P/E ratio" in observation
        for observation in result.observations
    )


def test_compare_requires_two_tickers() -> None:
    with pytest.raises(ValueError, match="At least two"):
        compare_stocks(["AAPL"])


def test_compare_rejects_duplicates() -> None:
    with pytest.raises(ValueError, match="Duplicate"):
        compare_stocks(["AAPL", "aapl"])


@patch("equity_snapshot.services.get_financial_snapshot")
def test_research_summary_positive_company(mock_snapshot) -> None:
    mock_snapshot.return_value = make_snapshot(
        ticker="TEST",
        revenue_growth=0.15,
        profit_margin=0.20,
        free_cash_flow=500,
        cash=1_000,
        total_debt=200,
        trailing_pe=22,
    )

    result = get_research_summary("TEST")

    assert "Revenue growth is positive." in result.strengths
    assert "The company is currently profitable." in result.strengths
    assert "Cash is greater than total debt." in result.strengths
    assert result.warnings == []


@patch("equity_snapshot.services.get_financial_snapshot")
def test_research_summary_warning_company(mock_snapshot) -> None:
    mock_snapshot.return_value = make_snapshot(
        ticker="TEST",
        revenue_growth=-0.10,
        profit_margin=-0.05,
        free_cash_flow=-500,
        cash=100,
        total_debt=600,
        trailing_pe=None,
    )

    result = get_research_summary("TEST")

    assert "Revenue growth is negative." in result.warnings
    assert "The company has a negative profit margin." in result.warnings
    assert "Total debt is greater than cash." in result.warnings
