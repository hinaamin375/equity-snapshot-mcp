"""Provider interface for equity snapshot operations."""

from collections.abc import Mapping
from typing import Any

import yfinance as yf

from equity_snapshot.exceptions import ProviderError, TickerNotFoundError
from equity_snapshot.models import CompanyProfile, DataSource, FinancialSnapshot
from equity_snapshot.validation import normalize_ticker


def _safe_float(value: Any) -> float | None:
    """Convert a provider value to float without crashing."""

    if value is None:
        return None

    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _load_info(ticker: str) -> tuple[str, Mapping[str, Any]]:
    normalized = normalize_ticker(ticker)

    try:
        stock = yf.Ticker(normalized)
        info = stock.info
    except Exception as exc:
        raise ProviderError(f"Failed to retrieve data for {normalized}.") from exc

    if not info or not info.get("symbol"):
        raise TickerNotFoundError(f"No company data was found for ticker {normalized}.")

    return normalized, info


def get_company_profile(ticker: str) -> CompanyProfile:
    normalized, info = _load_info(ticker)

    return CompanyProfile(
        ticker=normalized,
        company_name=info.get("longName") or info.get("shortName"),
        exchange=info.get("exchange"),
        sector=info.get("sector"),
        industry=info.get("industry"),
        currency=info.get("currency"),
        market_cap=_safe_float(info.get("marketCap")),
        description=info.get("longBusinessSummary"),
        source=DataSource(provider="Yahoo Finance via yfinance"),
    )


def get_financial_snapshot(ticker: str) -> FinancialSnapshot:
    normalized, info = _load_info(ticker)
    warnings: list[str] = []

    fields = {
        "revenue": _safe_float(info.get("totalRevenue")),
        "revenue_growth": _safe_float(info.get("revenueGrowth")),
        "net_income": _safe_float(info.get("netIncomeToCommon")),
        "profit_margin": _safe_float(info.get("profitMargins")),
        "free_cash_flow": _safe_float(info.get("freeCashflow")),
        "cash": _safe_float(info.get("totalCash")),
        "total_debt": _safe_float(info.get("totalDebt")),
        "trailing_pe": _safe_float(info.get("trailingPE")),
    }

    missing_fields = [name for name, value in fields.items() if value is None]

    if missing_fields:
        warnings.append("Unavailable fields: " + ", ".join(sorted(missing_fields)))

    return FinancialSnapshot(
        ticker=normalized,
        company_name=info.get("longName") or info.get("shortName"),
        currency=info.get("currency"),
        source=DataSource(provider="Yahoo Finance via yfinance"),
        warnings=warnings,
        **fields,
    )
