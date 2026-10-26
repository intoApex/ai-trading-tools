# TradingAgentStack MCP server

A small, **read-only** MCP server that lets Claude, Cursor and other MCP clients search the [TradingAgentStack](https://tradingagentstack.com) directory: AI trading agents, broker MCP servers, market data APIs, Telegram bots, agent wallets and exchanges. Each entry includes paper vs live trading, order approval, the published safety score, pricing, rate limits, an official source and a last-checked date.

It can't place trades or connect to any broker. It only reads the open dataset in [`../data/tools.json`](../data/tools.json) (CC BY 4.0).

## Tools

| Tool | What it does |
|---|---|
| `search_tools(query, category?, limit?)` | Keyword search, with an optional category filter |
| `get_tool(slug)` | Full record for one tool, e.g. `alpaca-mcp-server` |
| `compare_brokers(a, b)` | Side-by-side comparison of two tools |
| `list_categories()` | Categories with counts |

Example prompts: *"Which broker MCP servers support paper trading?"*, *"Compare Alpaca MCP and Tradier MCP on safety controls."*

## Install

Needs Node.js 18 or later.

### Claude Desktop

Add this to `claude_desktop_config.json` (Settings → Developer → Edit Config):

```json
{
  "mcpServers": {
    "tradingagentstack": { "command": "npx", "args": ["-y", "tradingagentstack-mcp"] }
  }
}
```

### Cursor

Add this to `~/.cursor/mcp.json` (or `.cursor/mcp.json` in a project):

```json
{
  "mcpServers": {
    "tradingagentstack": { "command": "npx", "args": ["-y", "tradingagentstack-mcp"] }
  }
}
```

### Claude Code

```bash
claude mcp add tradingagentstack -- npx -y tradingagentstack-mcp
```

### From source

```bash
git clone https://github.com/intoApex/ai-trading-tools && cd ai-trading-tools/mcp-server
npm install && npm test        # copies ../data/tools.json and runs a stdio smoke test
node src/index.js              # or point your client's "command" at this file
```

The server uses the dataset bundled with the package. To use the latest data from GitHub instead, set `TRADINGAGENTSTACK_LIVE=1`; it falls back to the bundled copy if the fetch fails.

## License

The code is MIT. The data is CC BY 4.0 and should be credited to TradingAgentStack (tradingagentstack.com). Not financial advice.
