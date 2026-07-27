from fastmcp import FastMCP

from equity_snapshot.provider import (
    get_company_profile as provider_get_company_profile,
)
from equity_snapshot.provider import (
    get_financial_snapshot as provider_get_financial_snapshot,
)
from equity_snapshot.services import (
    compare_stocks as service_compare_stocks,
)
from equity_snapshot.services import (
    get_research_summary as service_get_research_summary,
)


mcp = FastMCP(
    name="EquitySnapshot MCP",
    instructions=(
        "Use these tools to retrieve and compare public-company fundamental "
        "data. The data is for educational purposes only and should not be "
        "presented as financial advice."
    ),
)


@mcp.tool
def get_company_profile(ticker: str) -> dict:
    """Get basic company information for a stock ticker."""

    result = provider_get_company_profile(ticker)
    return result.model_dump(mode="json")


@mcp.tool
def get_financial_snapshot(ticker: str) -> dict:
    """Get a fundamental financial snapshot for a stock ticker."""

    result = provider_get_financial_snapshot(ticker)
    return result.model_dump(mode="json")


@mcp.tool
def compare_stocks(tickers: list[str]) -> dict:
    """Compare the fundamentals of two to five stock tickers."""

    result = service_compare_stocks(tickers)
    return result.model_dump(mode="json")


@mcp.tool
def get_research_summary(ticker: str) -> dict:
    """Return evidence-based strengths and warning signs for a stock."""

    result = service_get_research_summary(ticker)
    return result.model_dump(mode="json")


if __name__ == "__main__":
    mcp.run()
