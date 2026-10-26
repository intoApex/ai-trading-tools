#!/usr/bin/env python3
"""Regenerate data/tools.json, data/tools.csv and the README from TradingAgentStack.

Source of truth:
  https://tradingagentstack.com/data/tools.json
  https://tradingagentstack.com/data/tools.csv

The same JSON is published in https://github.com/intoApex/tas-ratings (CC BY 4.0).
The script writes those records locally and rebuilds the category tables.
It does not invent listings. Run it, then commit only if the files changed.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import re
import sys
import urllib.request
from pathlib import Path
from string import Template

ROOT = Path(__file__).resolve().parent.parent
JSON_URL = "https://tradingagentstack.com/data/tools.json"
CSV_URL = "https://tradingagentstack.com/data/tools.csv"
TEMPLATE = Path(__file__).resolve().parent / "readme_template.md"
USER_AGENT = "ai-trading-tools-sync/1.0 (+https://github.com/intoApex/ai-trading-tools)"

# Directory hubs and category pages that exist on tradingagentstack.com.
HUBS = [
    (
        "Trade with a bot",
        "https://tradingagentstack.com/trade-with-a-bot/",
        "hub-trade",
        [
            ("ai_trading_agent", "https://tradingagentstack.com/ai-trading-agents/"),
            ("ai_bot_platform", "https://tradingagentstack.com/ai-trading-bots/"),
            ("open_source_bot", "https://tradingagentstack.com/open-source-ai-trading-bots/"),
            ("defi_agent", "https://tradingagentstack.com/defi-trading-bots-and-agents/"),
            ("ai_signals", "https://tradingagentstack.com/ai-trading-signals/"),
            ("copy_trading", "https://tradingagentstack.com/copy-trading-platforms/"),
            ("agent_token", "https://tradingagentstack.com/ai-agent-tokens/"),
        ],
    ),
    (
        "Build an AI agent",
        "https://tradingagentstack.com/build-an-ai-agent/",
        "hub-build",
        [
            ("broker_mcp", "https://tradingagentstack.com/category/broker-mcp/"),
            ("data_mcp", "https://tradingagentstack.com/category/data-mcp/"),
            ("agent_framework", "https://tradingagentstack.com/category/agent-framework/"),
            ("risk_tool", "https://tradingagentstack.com/trading-bot-risk-safety-tools/"),
            ("agent_wallet", "https://tradingagentstack.com/ai-agent-wallets/"),
            ("agent_payments", "https://tradingagentstack.com/ai-agent-payments/"),
        ],
    ),
    (
        "Markets & infrastructure",
        "https://tradingagentstack.com/markets-and-infrastructure/",
        "hub-markets",
        [
            ("bot_exchange", "https://tradingagentstack.com/crypto-exchanges-for-trading-bots/"),
            ("prediction_market", "https://tradingagentstack.com/prediction-market-apis/"),
            ("broker_api", "https://tradingagentstack.com/category/broker-api/"),
            ("data_api", "https://tradingagentstack.com/category/data-api/"),
            ("backtest_platform", "https://tradingagentstack.com/category/backtest-platform/"),
            ("bot_vps", "https://tradingagentstack.com/vps-for-trading-bots/"),
        ],
    ),
]

CATEGORY_NOTES = {
    "defi_agent": "Guide: [Best Telegram trading bots](https://tradingagentstack.com/best-telegram-trading-bots/).",
}

REQUIRED = (
    "name",
    "slug",
    "url",
    "page",
    "category",
    "category_label",
    "assets_covered",
    "live_vs_paper",
    "official_or_community",
    "safety_pct",
    "safety_partial",
    "source",
    "last_checked",
)


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        if resp.status != 200:
            raise SystemExit(f"fetch failed: {url} status {resp.status}")
        return resp.read()


def load_dataset(json_bytes: bytes, csv_bytes: bytes) -> dict:
    try:
        data = json.loads(json_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SystemExit(f"tools.json is not valid JSON: {exc}") from exc
    if not isinstance(data, dict) or not isinstance(data.get("tools"), list):
        raise SystemExit("tools.json must be an object with a tools array")
    meta = data.get("meta") or {}
    tools = data["tools"]
    if not tools:
        raise SystemExit("tools.json contains no tools")
    if meta.get("count") != len(tools):
        raise SystemExit(f"meta.count {meta.get('count')} != {len(tools)} tools")
    if meta.get("license") != "CC BY 4.0":
        raise SystemExit(f"unexpected license: {meta.get('license')}")
    slugs = [t.get("slug") for t in tools]
    if len(slugs) != len(set(slugs)):
        raise SystemExit("duplicate slugs in tools.json")
    for t in tools:
        if not isinstance(t, dict):
            raise SystemExit("tool record is not an object")
        missing = [k for k in REQUIRED if k not in t]
        if missing:
            raise SystemExit(f"{t.get('name') or t.get('slug')}: missing {', '.join(missing)}")
        if t["page"] != f"https://tradingagentstack.com/tool/{t['slug']}/":
            raise SystemExit(f"{t['slug']}: page URL does not match its slug")
        if not isinstance(t["safety_pct"], int):
            raise SystemExit(f"{t['slug']}: safety_pct is not an integer")
        if not isinstance(t["assets_covered"], list):
            raise SystemExit(f"{t['slug']}: assets_covered is not a list")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(t["last_checked"])):
            raise SystemExit(f"{t['slug']}: bad last_checked")
        for key in t:
            if key.startswith("affiliate_"):
                raise SystemExit(f"{t['slug']}: affiliate field {key} is not allowed")
    text = csv_bytes.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    if not text.endswith(b"\n"):
        text += b"\n"
    rows = list(csv.DictReader(io.StringIO(text.decode("utf-8"))))
    csv_names = {r.get("name") for r in rows}
    json_names = {t["name"] for t in tools}
    if csv_names != json_names:
        raise SystemExit(
            f"CSV and JSON tool names differ: missing {sorted(json_names - csv_names)[:5]} extra {sorted(csv_names - json_names)[:5]}"
        )
    return {"data": data, "csv_text": text.decode("utf-8")}


def cell(value) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        value = ", ".join(str(v) for v in value)
    text = re.sub(r"\s+", " ", str(value).replace("\r", " ").replace("\n", " ")).strip()
    return text.replace("|", "\\|")


def safety_cell(tool: dict) -> str:
    pct = tool.get("safety_pct")
    if not isinstance(pct, int):
        return ""
    text = f"{pct}%"
    if tool.get("safety_partial"):
        text += " (partial)"
    return text


def agent_risk_cell(tool: dict) -> str:
    risk = tool.get("risk_v2")
    if not isinstance(risk, dict):
        return ""
    score, maximum = risk.get("score"), risk.get("max")
    if not isinstance(score, int) or not isinstance(maximum, int) or maximum <= 0:
        return ""
    pct = round(100 * score / maximum)
    text = f"{pct}%"
    if risk.get("partial"):
        text += " (partial)"
    return text


def tool_row(tool: dict) -> str:
    markets = list(tool.get("assets_covered") or [])
    if tool.get("former_names"):
        markets_text = cell(markets)
        extra = cell(tool["former_names"])
        markets_text = f"{markets_text}. Formerly: {extra}" if markets_text else f"Formerly: {extra}"
    else:
        markets_text = cell(markets)
    live = cell(tool.get("live_vs_paper"))
    if tool.get("status"):
        status = f"Status: {cell(tool['status'])}"
        live = f"{live}. {status}" if live else status
    name = cell(tool["name"])
    return (
        f"| [{name}]({tool['page']}) | {markets_text} | {live} | {cell(tool.get('official_or_community'))} "
        f"| {safety_cell(tool)} | {agent_risk_cell(tool)} |"
    )


def render_categories(tools: list[dict]) -> tuple[str, str]:
    by_cat: dict[str, list[dict]] = {}
    labels: dict[str, str] = {}
    for tool in tools:
        by_cat.setdefault(tool["category"], []).append(tool)
        labels.setdefault(tool["category"], tool["category_label"])
    for rows in by_cat.values():
        rows.sort(key=lambda t: t["name"].casefold())

    known = {cat for _, _, _, cats in HUBS for cat, _url in cats}
    toc = [
        "- [How scores work](#how-scores-work)",
    ]
    parts: list[str] = []
    header = "| Tool | Markets | Live or paper | Maintainer | Safety | Agent risk |\n|---|---|---|---|---|---|"

    def section(cat: str, url: str) -> str:
        rows = by_cat.get(cat) or []
        label = labels.get(cat, cat)
        lines = [
            f'<a id="cat-{cat}"></a>',
            "",
            f"### {label} ({len(rows)})",
            "",
            f"[{label} on TradingAgentStack]({url})",
            "",
        ]
        note = CATEGORY_NOTES.get(cat)
        if note:
            lines += [note, ""]
        lines += [header, *[tool_row(t) for t in rows], ""]
        return "\n".join(lines)

    for title, url, anchor, cats in HUBS:
        present = [c for c, _u in cats if c in by_cat]
        if not present:
            continue
        toc.append(f"- [{title}](#{anchor})")
        parts += [
            f'<a id="{anchor}"></a>',
            "",
            f"## {title}",
            "",
            f"See [{title}]({url}).",
            "",
        ]
        for cat, cat_url in cats:
            if cat not in by_cat:
                continue
            label = labels.get(cat, cat)
            toc.append(f"  - [{label} ({len(by_cat[cat])})](#cat-{cat})")
            parts.append(section(cat, cat_url))

    unknown = sorted((c for c in by_cat if c not in known), key=lambda c: labels.get(c, c).casefold())
    if unknown:
        toc.append("- [Other published categories](#hub-other)")
        parts += ['<a id="hub-other"></a>', "", "## Other published categories", ""]
        for cat in unknown:
            label = labels.get(cat, cat)
            toc.append(f"  - [{label} ({len(by_cat[cat])})](#cat-{cat})")
            parts.append(section(cat, "https://tradingagentstack.com/tools/"))

    rendered = sum(len(v) for v in by_cat.values())
    if rendered != len(tools):
        raise SystemExit(f"rendered {rendered} rows for {len(tools)} tools")
    toc += [
        "- [Sibling projects](#sibling-projects)",
        "- [Data source and license](#data-source-and-license)",
        "- [Contributing](#contributing)",
    ]
    return "\n".join(toc), "\n".join(parts).rstrip() + "\n"


def render_readme(data: dict) -> str:
    template = TEMPLATE.read_text(encoding="utf-8")
    if "\u2014" in template or "\u2013" in template:
        raise SystemExit("readme template contains an en dash or em dash")
    tools = data["tools"]
    meta = data.get("meta") or {}
    toc, categories = render_categories(tools)
    readme = Template(template).substitute(
        count=str(len(tools)),
        generated=str(meta.get("generated") or max(t["last_checked"] for t in tools)),
        last_checked=max(t["last_checked"] for t in tools),
        toc=toc,
        categories=categories.rstrip(),
    )
    if "$count" in readme or "$categories" in readme:
        raise SystemExit("readme template placeholders were not filled")
    if not readme.endswith("\n"):
        readme += "\n"
    return readme


def write_outputs(dataset: dict) -> None:
    pretty = json.dumps(dataset["data"], indent=2, ensure_ascii=False) + "\n"
    # Stable on the next run: the same parser and serializer must round-trip.
    if json.dumps(json.loads(pretty), indent=2, ensure_ascii=False) + "\n" != pretty:
        raise SystemExit("JSON serializer is not stable")
    readme = render_readme(dataset["data"])
    (ROOT / "data").mkdir(exist_ok=True)
    (ROOT / "data" / "tools.json").write_text(pretty, encoding="utf-8")
    (ROOT / "data" / "tools.csv").write_text(dataset["csv_text"], encoding="utf-8")
    (ROOT / "README.md").write_text(readme, encoding="utf-8")
    print(
        f"synced {len(dataset['data']['tools'])} tools, generated {dataset['data'].get('meta', {}).get('generated')}"
    )


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Sync the AI trading tools list from TradingAgentStack")
    parser.add_argument("--json", type=Path, help="Local tools.json instead of the live URL")
    parser.add_argument("--csv", type=Path, help="Local tools.csv instead of the live URL")
    args = parser.parse_args(argv)
    if bool(args.json) != bool(args.csv):
        raise SystemExit("pass both --json and --csv, or neither to fetch the live dataset")
    if args.json:
        json_bytes = args.json.read_bytes()
        csv_bytes = args.csv.read_bytes()
    else:
        json_bytes = fetch(JSON_URL)
        csv_bytes = fetch(CSV_URL)
    write_outputs(load_dataset(json_bytes, csv_bytes))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
