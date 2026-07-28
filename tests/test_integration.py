import pytest

from equity_snapshot.provider import get_company_profile


@pytest.mark.integration
def test_live_company_profile() -> None:
    result = get_company_profile("AAPL")

    assert result.ticker == "AAPL"
    assert result.company_name
    assert result.source.provider