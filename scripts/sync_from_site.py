"""Regenerate data/tools.json, data/tools.csv and the README tables from TradingAgentStack's listings.json.
Usage: python scripts/sync_from_site.py path/to/listings.json"""
import csv, json, re, sys, pathlib
R = pathlib.Path(__file__).resolve().parent.parent
CAT = {"broker_mcp":"Broker MCP servers","data_mcp":"Market data MCP servers","broker_api":"Broker APIs","data_api":"Market data APIs","agent_framework":"Agent frameworks","backtest_platform":"Backtesting","trading_agent":"Trading agents","security_tool":"Security","ai_bot_platform":"AI trading bot platforms","open_source_bot":"Open-source trading bots","bot_exchange":"Exchanges & brokers for bots","ai_signals":"AI signals & research copilots"}
slug = lambda s: re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')
src = json.load(open(sys.argv[1]))
old = {x["name"]: x for x in json.load(open(R/"data/tools.json"))}
oldtype = {}
for line in open(R/"README.md"):
    m = re.match(r"\| \[(.+?)\]\(.*?\) \| .* \| ([^|]+?) \| [^|]+ \| \[details\]", line)
    if m: oldtype[m.group(1)] = m.group(2)
out = []
for x in src:
    y = {k: v for k, v in x.items() if not k.startswith("affiliate_")}; y["details_url"] = f"https://tradingagentstack.com/tool/{slug(x['name'])}/"
    out.append(y)
json.dump(out, open(R/"data/tools.json", "w"), indent=2, ensure_ascii=False); open(R/"data/tools.json","a").write("\n")
cols = ["name","url","category","assets_covered","live_vs_paper","order_approval_safety","pricing_free_tier","rate_limits","official_or_community","repo","former_names","status","source","sources","last_checked","details_url"]
extra = sorted({k for x in out for k in x} - set(cols)); cols += extra
with open(R/"data/tools.csv", "w", newline="") as f:
    w = csv.DictWriter(f, cols); w.writeheader()
    for x in out: w.writerow({k: "; ".join(v) if isinstance(v, list) else v for k, v in x.items()})
md = open(R/"README.md").read()
cell = lambda s: str(s).replace("|", "\\|").replace("\n", " ")
for k, v in CAT.items():
    rows = []
    for x in sorted(out, key=lambda x: x["name"].lower()):
        if x["category"] != k: continue
        t = {"ai_bot_platform":"Bot platform","open_source_bot":"Open-source bot","bot_exchange":"Exchange","ai_signals":"Signals / research"}.get(k) or oldtype.get(x["name"]) or ("MCP" if k.endswith("mcp") else "API")
        d = f"{', '.join(x['assets_covered'])}. {x['live_vs_paper']}"
        if x.get("status"): d += f". **Status:** {x['status']}"
        rows.append(f"| [{cell(x['name'])}]({x['url']}) | {cell(d)} | {t} | {x['official_or_community']} | [details]({x['details_url']}) |")
    hdr = "| Tool | Description | Type | Official / community | Details |\n|---|---|---|---|---|\n"
    md = re.sub(rf"(## {re.escape(v)}\n\n(?:[^|\n].*\n\n)?{re.escape(hdr)})(?:\|.*\n)*", lambda m: m.group(1) + "\n".join(rows) + "\n", md)
md = re.sub(r"\*\*\d+ tools\*\* · Last verified: \*\*[\d-]+\*\*", f"**{len(out)} tools** · Last verified: **{max(x['last_checked'] for x in out)}**", md)
open(R/"README.md", "w").write(md)
print("synced", len(out))
