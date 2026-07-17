# EquitySnapshot MCP

A minimal stock-research MCP server that gives AI assistants access to
normalized company profiles and fundamental financial snapshots.

## Current status

Day 1: data-provider layer implemented.

## Planned MCP tools

- `get_company_profile`
- `get_financial_snapshot`
- `compare_stocks`
- `get_research_summary`

## Technology

- Python
- Pydantic
- yfinance
- FastMCP
- pytest

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
python scripts/try_snapshot.py AAPL