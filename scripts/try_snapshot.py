import argparse
import json

from equity_snapshot.exceptions import StockResearchError
from equity_snapshot.provider import (
    get_company_profile,
    get_financial_snapshot,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Retrieve a company profile and financial snapshot."
    )
    parser.add_argument("ticker", help="Ticker symbol, such as AAPL")
    args = parser.parse_args()

    try:
        profile = get_company_profile(args.ticker)
        snapshot = get_financial_snapshot(args.ticker)
    except StockResearchError as exc:
        raise SystemExit(f"Error: {exc}") from exc

    output = {
        "profile": profile.model_dump(mode="json"),
        "financial_snapshot": snapshot.model_dump(mode="json"),
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
