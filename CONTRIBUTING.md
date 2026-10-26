# Contributing

Thanks for helping keep this list accurate. The README tables and `data/tools.json` are regenerated from the public TradingAgentStack dataset by `scripts/sync_from_site.py`. A weekly GitHub Action commits that refresh when the published data changes.

## Three ways to contribute

1. **Upstream correction:** submit the official source at https://tradingagentstack.com/submit/. That is the dataset this list copies.
2. **Issue:** open an issue with the **Add or update a tool** template, including a link to the vendor's own docs.
3. **Pull request:** for a fix to the sync script, the README template, or the MCP server. Do not hand-edit the generated category tables. They will be overwritten on the next sync.

## What a listing needs

Facts have to come from the vendor's own docs or another source TradingAgentStack can check. The open dataset uses these fields:

| Field | Description |
|---|---|
| `name` | Official product name |
| `url` | Official docs or product page |
| `category` | Directory category, such as `broker_mcp`, `data_api`, `ai_trading_agent`, `defi_agent`, `agent_wallet`, `bot_exchange` |
| `assets_covered` | Markets or data covered |
| `live_vs_paper` | Live, paper, demo, testnet, or data only |
| `order_approval_safety` | How orders are approved, scoped or limited |
| `pricing_free_tier` | Pricing and any free tier |
| `rate_limits` | Published API rate limits, or unknown |
| `official_or_community` | `official`, `community`, `academic` or `third-party` |
| `source` | URL that backs the facts |
| `safety_pct` | Safety score percentage published by TradingAgentStack |

`page` and `slug` point at `https://tradingagentstack.com/tool/{slug}/`. Safety inputs and Agent Risk Scores are copied from the dataset. They are not edited in this repo.

## Rules

- No affiliate links or tracking parameters.
- Do not invent scores, prices or safety claims. If a fact has no official source, leave it unknown.
- Vendors are welcome to suggest their own tools. Say so in the issue.

By contributing, you agree that your contribution is licensed under CC BY 4.0.
