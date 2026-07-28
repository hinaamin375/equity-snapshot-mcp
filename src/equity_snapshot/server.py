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
    """
    Retrieve basic public-company information for one stock ticker.

    Use this tool for company name, sector, industry, exchange,
    market capitalization, currency, and business description.
    """

    result = provider_get_company_profile(ticker)
    return result.model_dump(mode="json")


@mcp.tool
def get_financial_snapshot(ticker: str) -> dict:
    """
    Retrieve a normalized fundamental snapshot for one stock ticker.

    Returns revenue, growth, profit margin, cash, debt,
    free cash flow, and trailing P/E when available.
    """
    result = provider_get_financial_snapshot(ticker)
    return result.model_dump(mode="json")


@mcp.tool
def compare_stocks(tickers: list[str]) -> dict:
    """
    Compare two to five public-company tickers using the same
    normalized fundamental metrics.

    Use this tool when the user asks which company has higher
    growth, profitability, free cash flow, or a lower trailing P/E.
    """
    result = service_compare_stocks(tickers)
    return result.model_dump(mode="json")


@mcp.tool
def get_research_summary(ticker: str) -> dict:
    """
    Produce deterministic, evidence-based strengths, warnings,
    and neutral observations for one stock.

    This tool does not provide buy or sell recommendations.
    """
    result = service_get_research_summary(ticker)
    return result.model_dump(mode="json")


if __name__ == "__main__":
    mcp.run()
