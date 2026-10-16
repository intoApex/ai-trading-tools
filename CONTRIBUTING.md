# Contributing

Thanks for helping keep this list accurate. Every entry must link to an official or verifiable source.

## Three ways to contribute

1. **Pull request:** edit `data/tools.json` (and add the same row to `data/tools.csv` and the right README table). One tool per PR, please.
2. **Issue:** open an issue with the **Add or update a tool** template.
3. **Web form:** submit at https://tradingagentstack.com/submit/

## Required fields

| Field | Description |
|---|---|
| `name` | Official product name |
| `url` | Official docs or product page |
| `category` | One of `broker_mcp`, `data_mcp`, `broker_api`, `data_api`, `agent_framework`, `backtest_platform`, `trading_agent`, `security_tool` |
| `assets_covered` | List, e.g. `["US stocks", "options", "crypto"]` |
| `live_vs_paper` | Live trading, paper trading, or both |
| `order_approval_safety` | How orders are approved or limited (read-only modes, confirmations, scoped toolsets) |
| `pricing_free_tier` | Pricing and any free tier |
| `rate_limits` | Published API rate limits, or "not published" |
| `official_or_community` | `official` (built by the vendor) or `community` |
| `source` | URL that backs the facts above |

Optional: `repo` (source code URL), `former_names`, `sources`, `status` (e.g. a product being wound down). `details_url` is generated.

## Rules

- No affiliate links or tracking parameters.
- Facts must come from the vendor's own docs or a linked source. We re-verify listings regularly and set `last_checked` ourselves.
- Vendors are welcome to submit their own tools. Please say so in the PR or issue.

By contributing, you agree that your contribution is licensed under CC BY 4.0.
