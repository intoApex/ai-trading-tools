# AI Trading Tools: the open list of tools that connect AI agents to markets

An open, sourced dataset of the broker MCP servers, market data APIs, agent frameworks and backtesters that let AI agents trade and research markets. Every entry links to an official source. Maintained by [TradingAgentStack](https://tradingagentstack.com), where each tool has a full page with pricing, rate limits, paper vs live trading and safety controls.

**41 tools** · Last verified: **2026-10-16** · Data: [`data/tools.json`](data/tools.json) · [`data/tools.csv`](data/tools.csv) · License: [CC BY 4.0](LICENSE)

📬 Get new tools and changes weekly: [subscribe to the TradingAgentStack newsletter](https://tradingagentstack.com/#nle).

> Not financial advice. Verify details with each vendor before connecting real money.

## Contents

- [Broker MCP servers](#broker-mcp-servers)
- [Market data MCP servers](#market-data-mcp-servers)
- [Broker APIs](#broker-apis)
- [Market data APIs](#market-data-apis)
- [Agent frameworks](#agent-frameworks)
- [Backtesting](#backtesting)
- [Trading agents](#trading-agents)
- [Security](#security)

## Broker MCP servers

| Tool | Description | Type | Official / community | Details |
|---|---|---|---|---|
| [Alpaca MCP Server](https://docs.alpaca.markets/us/docs/trading-api-mcp) | US stocks, ETFs, options, crypto, fixed income quotes. live and paper (ALPACA_PAPER_TRADE defaults to true/paper; paper with simulated $100K) | MCP | official | [details](https://tradingagentstack.com/tool/alpaca-mcp-server/) |
| [Axi MCP (MT5)](https://www.axi.com/int/trading-platforms/mcp) | Axi MT5 account instruments (live prices, candles, positions, orders). live and demo MT5 accounts; MT4 and Axi platform accounts view-only | MCP | official | [details](https://tradingagentstack.com/tool/axi-mcp-mt5/) |
| [Interactive Brokers AI Integration (MCP)](https://www.interactivebrokers.com/en/general/about/mediaRelations/7-28-26.php) | global multi-asset (account/portfolio, market data). live account | MCP | official | [details](https://tradingagentstack.com/tool/interactive-brokers-ai-integration-mcp/) |
| [Longbridge MCP](https://open.longbridge.com/docs/mcp) | quotes/depth, fundamentals, options, warrants. live trading tools (place/modify/cancel) | MCP | official | [details](https://tradingagentstack.com/tool/longbridge-mcp/) |
| [moomoo MCP](https://open.moomoo.com/mcp-docs/overview) | quotes, portfolio, orders; HK, US, CN, SG, JP, MY markets (OpenAPI). live trading capability | MCP | official | [details](https://tradingagentstack.com/tool/moomoo-mcp/) |
| [NinjaTrader MCP (beta)](https://docs.ninjatrader.com/mcp.md) | NinjaTrader account (contracts, quotes, orders, risk). Demo (simulated) and Live endpoints | MCP | official | [details](https://tradingagentstack.com/tool/ninjatrader-mcp-beta/) |
| [Public Hosted MCP Server](https://public.com/api/docs/templates/hosted-mcp) | Public.com brokerage account. live (real money) | MCP | official | [details](https://tradingagentstack.com/tool/public-hosted-mcp-server/) |
| [Robinhood Trading MCP](https://robinhood.com/us/en/support/articles/onboarding-an-external-agent/) | equities (long), options, crypto. live, from a dedicated MCP account | MCP | official | [details](https://tradingagentstack.com/tool/robinhood-trading-mcp/) |
| [tastytrade MCP Server](https://developer.tastytrade.com/docs/sdks-and-tools/mcp-server/) | tastytrade account (orders, quotes). live; sandbox available | MCP | official | [details](https://tradingagentstack.com/tool/tastytrade-mcp-server/) |
| [TradeStation MCP](https://www.tradestation.com/platforms-and-tools/mcp/) | TradeStation execution, market data, account APIs. live | MCP | official | [details](https://tradingagentstack.com/tool/tradestation-mcp/) |
| [Tradier MCP Server](https://tradier.com/develop/mcp-server) | US stocks, options (single-leg and multi-leg). live and paper (PAPER_TRADING flag with your paper token) | MCP | official | [details](https://tradingagentstack.com/tool/tradier-mcp-server/) |
| [Webull Cloud MCP Server](https://developer.webull.com/apis/docs/AI-friendly-Resources/mcp) | stocks, ETFs, options, futures, crypto, event contracts. live: creates order instructions (stocks, options, futures, crypto, event contracts, algo) that you confirm in the Webull app/desktop; plus account data, order history, market data | MCP | official | [details](https://tradingagentstack.com/tool/webull-cloud-mcp-server/) |

## Market data MCP servers

| Tool | Description | Type | Official / community | Details |
|---|---|---|---|---|
| [Alpha Vantage MCP](https://github.com/alphavantage/alpha_vantage_mcp) | stocks (20+ yrs history), quotes. data only | MCP | official | [details](https://tradingagentstack.com/tool/alpha-vantage-mcp/) |
| [Databento MCP servers (dbn-go)](https://github.com/NimbleMarkets/dbn-go/blob/main/cmd/README.md) | Databento datasets. data only | MCP | community | [details](https://tradingagentstack.com/tool/databento-mcp-servers-dbn-go/) |
| [Massive (formerly Polygon) MCP](https://massive.com/docs/ai-tools/quickstart) | stocks, options, forex, crypto, futures, fundamentals, news. data only | MCP | official | [details](https://tradingagentstack.com/tool/massive-formerly-polygon-mcp/) |
| [Pyth Pro MCP Server](https://docs.pyth.network/price-feeds/pro/mcp) | crypto, FX, equities, metals, rates, commodities, funding rates, NAVs. data only | MCP | official | [details](https://tradingagentstack.com/tool/pyth-pro-mcp-server/) |
| [TradingView MCP Server](https://www.tradingview.com/support/solutions/43000795699-mcp-server-connect-your-ai-assistant-to-tradingview/) | stocks, ETFs, forex, crypto, futures, indices, bonds, macro. no trading (watchlists/alerts only) | MCP | official | [details](https://tradingagentstack.com/tool/tradingview-mcp-server/) |

## Broker APIs

| Tool | Description | Type | Official / community | Details |
|---|---|---|---|---|
| [Alpaca Trading API](https://alpaca.markets/) | US stocks, ETFs, options, crypto. live and paper | API | official | [details](https://tradingagentstack.com/tool/alpaca-trading-api/) |
| [Interactive Brokers API](https://www.interactivebrokers.com/) | global stocks, options, futures, forex. live and paper | API | official | [details](https://tradingagentstack.com/tool/interactive-brokers-api/) |
| [Schwab Trader API](https://developer.schwab.com/) | US stocks, options. live | API | official | [details](https://tradingagentstack.com/tool/schwab-trader-api/) |
| [Tradier Brokerage API](https://tradier.com/) | US stocks, options. live and paper (sandbox) | API | official | [details](https://tradingagentstack.com/tool/tradier-brokerage-api/) |

## Market data APIs

| Tool | Description | Type | Official / community | Details |
|---|---|---|---|---|
| [Alpha Vantage API](https://www.alphavantage.co/) | stocks, ETFs, mutual funds, indices, options, forex, commodities, economic indicators, news & sentiment. data only | API | official | [details](https://tradingagentstack.com/tool/alpha-vantage-api/) |
| [Databento](https://databento.com/) | US equities, US futures, US options, crypto, FX. data only | API | official | [details](https://tradingagentstack.com/tool/databento/) |
| [Kalshi API](https://kalshi.com/) | prediction markets. live | API | official | [details](https://tradingagentstack.com/tool/kalshi-api/) |
| [Massive (Polygon) API](https://massive.com/) | stocks, options, indices, forex. data only | API | official | [details](https://tradingagentstack.com/tool/massive-polygon-api/) |
| [OpenBB](https://openbb.co/) | multi-provider wrapper. data only. **Status:** Company winding down (announced Aug 25, 2026). Code released under Apache 2.0 and maintained by the non-profit OpenBQ (github.com/openbq-org). | API | official | [details](https://tradingagentstack.com/tool/openbb/) |
| [Polymarket API](https://docs.polymarket.com/) | prediction markets. live | API | official | [details](https://tradingagentstack.com/tool/polymarket-api/) |
| [SEC EDGAR APIs](https://www.sec.gov/search-filings/edgar-application-programming-interfaces) | US filings/XBRL fundamentals. data only | API | official | [details](https://tradingagentstack.com/tool/sec-edgar-apis/) |
| [ThetaData](https://www.thetadata.net/) | stocks, options, indices, interest rates. data only | API | official | [details](https://tradingagentstack.com/tool/thetadata/) |
| [yfinance](https://github.com/ranaroussi/yfinance) | stocks, options chains. data only | API | community | [details](https://tradingagentstack.com/tool/yfinance/) |

## Agent frameworks

| Tool | Description | Type | Official / community | Details |
|---|---|---|---|---|
| [LangGraph](https://github.com/langchain-ai/langgraph) | n/a. n/a | Framework | official | [details](https://tradingagentstack.com/tool/langgraph/) |
| [LlamaIndex](https://github.com/run-llama/llama_index) | n/a. n/a | Framework | official | [details](https://tradingagentstack.com/tool/llamaindex/) |
| [Mastra](https://github.com/mastra-ai/mastra) | n/a. n/a | Framework | official | [details](https://tradingagentstack.com/tool/mastra/) |
| [Microsoft Agent Framework](https://github.com/microsoft/agent-framework) | n/a. n/a | Framework | official | [details](https://tradingagentstack.com/tool/microsoft-agent-framework/) |

## Backtesting

| Tool | Description | Type | Official / community | Details |
|---|---|---|---|---|
| [Backtesting.py](https://github.com/kernc/backtesting.py) | any (bring data). backtest only | Backtester | official | [details](https://tradingagentstack.com/tool/backtesting-py/) |
| [NautilusTrader](https://nautilustrader.io/) | multi-venue incl. IBKR and crypto. backtest and live | Backtester | official | [details](https://tradingagentstack.com/tool/nautilustrader/) |
| [QuantConnect / LEAN](https://www.quantconnect.com/) | equities, forex, futures, options, crypto. backtest, paper, live | Backtester | official | [details](https://tradingagentstack.com/tool/quantconnect-lean/) |
| [VectorBT](https://github.com/polakowo/vectorbt) | any (bring data). backtest/research only | Backtester | official | [details](https://tradingagentstack.com/tool/vectorbt/) |

## Trading agents

| Tool | Description | Type | Official / community | Details |
|---|---|---|---|---|
| [Agent Market Arena (AMA)](https://github.com/The-FinAI/Agent_Market_Arena) | crypto, stocks. live benchmark | Agent | academic | [details](https://tradingagentstack.com/tool/agent-market-arena-ama/) |
| [Freqtrade](https://github.com/freqtrade/freqtrade) | crypto. dry-run and live | Agent | official | [details](https://tradingagentstack.com/tool/freqtrade/) |

## Security

| Tool | Description | Type | Official / community | Details |
|---|---|---|---|---|
| [Canopii Trust Index](https://index.canopii.dev/) | MCP servers (any). n/a | Security tool | third-party | [details](https://tradingagentstack.com/tool/canopii-trust-index/) |

## Use it from Claude or Cursor (MCP server)

Search this dataset straight from your AI client with the read-only [TradingAgentStack MCP server](mcp-server/): `search_tools`, `get_tool`, `compare_brokers`, `list_categories`.

## Contributing

Know a tool we're missing, or spotted something out of date? See [CONTRIBUTING.md](CONTRIBUTING.md), open an issue, or [submit it on tradingagentstack.com](https://tradingagentstack.com/submit/).

## License

The data is licensed under [CC BY 4.0](LICENSE). Please credit **TradingAgentStack (tradingagentstack.com)**.
