from equity_snapshot.models import (
    ResearchSummary,
    StockComparison,
    StockComparisonItem,
)
from equity_snapshot.provider import get_financial_snapshot
from equity_snapshot.validation import normalize_ticker


MAX_COMPARISON_TICKERS = 5


def compare_stocks(tickers: list[str]) -> StockComparison:
    """Compare the fundamental snapshots of multiple stocks."""

    if not isinstance(tickers, list):
        raise ValueError("Tickers must be provided as a list.")

    if len(tickers) < 2:
        raise ValueError("At least two tickers are required for comparison.")

    if len(tickers) > MAX_COMPARISON_TICKERS:
        raise ValueError(f"A maximum of {MAX_COMPARISON_TICKERS} tickers may be compared.")

    normalized_tickers = [normalize_ticker(ticker) for ticker in tickers]

    if len(set(normalized_tickers)) != len(normalized_tickers):
        raise ValueError("Duplicate tickers are not allowed.")

    snapshots = [get_financial_snapshot(ticker) for ticker in normalized_tickers]

    companies = [
        StockComparisonItem(
            ticker=snapshot.ticker,
            company_name=snapshot.company_name,
            revenue_growth=snapshot.revenue_growth,
            profit_margin=snapshot.profit_margin,
            free_cash_flow=snapshot.free_cash_flow,
            cash=snapshot.cash,
            total_debt=snapshot.total_debt,
            trailing_pe=snapshot.trailing_pe,
            warnings=snapshot.warnings,
        )
        for snapshot in snapshots
    ]

    observations = _build_comparison_observations(companies)

    return StockComparison(
        tickers=normalized_tickers,
        companies=companies,
        observations=observations,
    )


def _build_comparison_observations(
    companies: list[StockComparisonItem],
) -> list[str]:
    observations: list[str] = []

    _add_highest_observation(
        companies=companies,
        field_name="revenue_growth",
        label="revenue growth",
        observations=observations,
    )

    _add_highest_observation(
        companies=companies,
        field_name="profit_margin",
        label="profit margin",
        observations=observations,
    )

    _add_highest_observation(
        companies=companies,
        field_name="free_cash_flow",
        label="free cash flow",
        observations=observations,
    )

    _add_lowest_observation(
        companies=companies,
        field_name="trailing_pe",
        label="trailing P/E ratio",
        observations=observations,
    )

    return observations


def _add_highest_observation(
    companies: list[StockComparisonItem],
    field_name: str,
    label: str,
    observations: list[str],
) -> None:
    available = [company for company in companies if getattr(company, field_name) is not None]

    if not available:
        return

    highest = max(
        available,
        key=lambda company: getattr(company, field_name),
    )

    observations.append(f"{highest.ticker} has the highest {label} among the compared stocks.")


def _add_lowest_observation(
    companies: list[StockComparisonItem],
    field_name: str,
    label: str,
    observations: list[str],
) -> None:
    available = [company for company in companies if getattr(company, field_name) is not None]

    if not available:
        return

    lowest = min(
        available,
        key=lambda company: getattr(company, field_name),
    )

    observations.append(f"{lowest.ticker} has the lowest {label} among the compared stocks.")


def get_research_summary(ticker: str) -> ResearchSummary:
    """Build simple evidence-based observations for a stock."""

    snapshot = get_financial_snapshot(ticker)

    strengths: list[str] = []
    warnings: list[str] = []
    neutral_observations: list[str] = []

    if snapshot.revenue_growth is not None:
        if snapshot.revenue_growth > 0:
            strengths.append("Revenue growth is positive.")
        elif snapshot.revenue_growth < 0:
            warnings.append("Revenue growth is negative.")
        else:
            neutral_observations.append("Revenue growth is flat.")

    if snapshot.profit_margin is not None:
        if snapshot.profit_margin > 0:
            strengths.append("The company is currently profitable.")
        else:
            warnings.append("The company has a negative profit margin.")

    if snapshot.free_cash_flow is not None:
        if snapshot.free_cash_flow > 0:
            strengths.append("The company generated positive free cash flow.")
        elif snapshot.free_cash_flow < 0:
            warnings.append("The company generated negative free cash flow.")

    if snapshot.cash is not None and snapshot.total_debt is not None:
        if snapshot.cash > snapshot.total_debt:
            strengths.append("Cash is greater than total debt.")
        elif snapshot.total_debt > snapshot.cash:
            warnings.append("Total debt is greater than cash.")
        else:
            neutral_observations.append("Cash and total debt are approximately equal.")

    if snapshot.trailing_pe is not None:
        neutral_observations.append(f"The trailing P/E ratio is {snapshot.trailing_pe:.2f}.")

    warnings.extend(snapshot.warnings)

    return ResearchSummary(
        ticker=snapshot.ticker,
        strengths=strengths,
        warnings=warnings,
        neutral_observations=neutral_observations,
    )
