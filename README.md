# Equity Snapshot MCP

Equity Snapshot MCP is a lightweight Model Context Protocol (MCP) server for retrieving public-company fundamentals and comparing stocks. It exposes a small set of tools that return normalized financial data from Yahoo Finance via the `yfinance` package.

## Features

The server currently provides four MCP tools:

- `get_company_profile`: returns basic company metadata such as company name, exchange, sector, industry, market capitalization, currency, and business description.
- `get_financial_snapshot`: returns a normalized financial snapshot with metrics such as revenue, revenue growth, net income, profit margin, free cash flow, cash, total debt, and trailing P/E ratio.
- `compare_stocks`: compares two to five tickers and highlights simple relative observations about profitability, growth, cash flow, and valuation.
- `get_research_summary`: produces a deterministic, evidence-based summary of strengths, warnings, and neutral observations for a single ticker.

## Installation

Requirements:

- Python 3.11 or newer

Install from the repository root:

```bash
pip install -e .
```

To install development dependencies as well:

```bash
pip install -e .[dev]
```

## Running the server

From the repository root, run:

```bash
python -m equity_snapshot.server
```

If you installed the package in editable mode, the console script is also available:

```bash
equity-snapshot-mcp
```

## Example tool usage

### Get a company profile

```json
{
  "ticker": "AAPL"
}
```

### Get a financial snapshot

```json
{
  "ticker": "MSFT"
}
```

### Compare two or more stocks

```json
{
  "tickers": ["AAPL", "MSFT", "NVDA"]
}
```

### Get a research summary

```json
{
  "ticker": "TSLA"
}
```

## Development

Run the test suite:

```bash
pytest
```

Run integration tests that call live external services:

```bash
pytest -m integration
```

Lint the project:

```bash
ruff check .
```

## Notes

- Data is sourced from Yahoo Finance and may be delayed or incomplete depending on the provider response.
- The tool outputs are intended for educational and research purposes only and should not be treated as financial advice.

## License

This project is licensed under the MIT License.