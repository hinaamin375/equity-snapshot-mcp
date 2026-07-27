## MCP tools

### `get_company_profile`

Returns:

- Company name
- Exchange
- Sector
- Industry
- Market capitalization
- Business description

### `get_financial_snapshot`

Returns:

- Revenue
- Revenue growth
- Net income
- Profit margin
- Free cash flow
- Cash
- Total debt
- Trailing P/E ratio

### `compare_stocks`

Compares two to five tickers using normalized fundamental metrics.

Example input:

```json
{
  "tickers": ["AAPL", "MSFT"]
}