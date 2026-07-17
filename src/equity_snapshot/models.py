"""Data models for equity snapshot data."""

from datetime import datetime, timezone

from pydantic import BaseModel, Field


class DataSource(BaseModel):
    provider: str
    retrieved_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class CompanyProfile(BaseModel):
    ticker: str
    company_name: str | None = None
    exchange: str | None = None
    sector: str | None = None
    industry: str | None = None
    currency: str | None = None
    market_cap: float | None = None
    description: str | None = None
    source: DataSource


class FinancialSnapshot(BaseModel):
    ticker: str
    company_name: str | None = None
    currency: str | None = None

    revenue: float | None = None
    revenue_growth: float | None = None
    net_income: float | None = None
    profit_margin: float | None = None
    free_cash_flow: float | None = None
    cash: float | None = None
    total_debt: float | None = None
    trailing_pe: float | None = None

    source: DataSource
    warnings: list[str] = Field(default_factory=list)
