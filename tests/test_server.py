from equity_snapshot.server import mcp


def test_mcp_server_exists() -> None:
    assert mcp is not None
    assert mcp.name == "EquitySnapshot MCP"
