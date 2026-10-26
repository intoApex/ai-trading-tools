import { readFileSync } from "node:fs";

export const DATA_URL = "https://raw.githubusercontent.com/intoApex/ai-trading-tools/main/data/tools.json";
export const slug = (s) => s.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");

const PREFERRED = [
  "ai_trading_agent", "ai_bot_platform", "open_source_bot", "defi_agent", "ai_signals", "copy_trading", "agent_token",
  "broker_mcp", "data_mcp", "agent_framework", "risk_tool", "agent_wallet", "agent_payments",
  "bot_exchange", "prediction_market", "broker_api", "data_api", "backtest_platform", "bot_vps",
];

export function asTools(data) {
  const list = Array.isArray(data) ? data : data?.tools;
  if (!Array.isArray(list)) throw new Error("tools.json: expected an array or { tools: [] }");
  return list.map((t) => ({
    ...t,
    slug: t.slug || slug(t.name),
    details_url: t.details_url || t.page || `https://tradingagentstack.com/tool/${t.slug || slug(t.name)}/`,
  }));
}

export function categoriesFrom(tools) {
  const labels = new Map();
  for (const t of tools) {
    if (!labels.has(t.category)) labels.set(t.category, t.category_label || t.category);
  }
  const ids = [
    ...PREFERRED.filter((id) => labels.has(id)),
    ...[...labels.keys()].filter((id) => !PREFERRED.includes(id)),
  ];
  return Object.fromEntries(ids.map((id) => [id, labels.get(id)]));
}

export function loadBundled() {
  return asTools(JSON.parse(readFileSync(new URL("../data/tools.json", import.meta.url), "utf8")));
}

/** Try the live public dataset (TRADINGAGENTSTACK_LIVE=1), fall back to the bundled copy. */
export async function loadTools() {
  if (process.env.TRADINGAGENTSTACK_LIVE === "1") {
    try {
      const r = await fetch(DATA_URL, { signal: AbortSignal.timeout(5000) });
      if (r.ok) return asTools(await r.json());
    } catch {}
  }
  return loadBundled();
}

const text = (t) => [t.name, t.category, t.category_label, t.safety_level, t.who_places_order, ...(t.assets_covered || []),
  t.live_vs_paper, t.order_approval_safety, t.pricing_free_tier, t.official_or_community, t.status, t.former_names]
  .flat().filter(Boolean).join(" ").toLowerCase();

export function searchTools(tools, query = "", category) {
  const terms = query.toLowerCase().split(/\s+/).filter(Boolean);
  return tools
    .filter((t) => !category || t.category === category)
    .map((t) => {
      const hay = text(t), name = t.name.toLowerCase();
      const score = terms.reduce((s, w) => s + (name.includes(w) ? 3 : 0) + (hay.includes(w) ? 1 : 0), 0);
      return { t, score };
    })
    .filter(({ score }) => terms.length === 0 || score > 0)
    .sort((a, b) => b.score - a.score || a.t.name.localeCompare(b.t.name))
    .map(({ t }) => t);
}

export function findTool(tools, q) {
  const s = slug(q);
  return tools.find((t) => t.slug === s) || tools.find((t) => t.slug.includes(s)) || tools.find((t) => slug(t.name).startsWith(s.split("-")[0]) && s.length > 2);
}

export const summary = (t) => ({
  slug: t.slug, name: t.name, category: t.category, category_label: t.category_label || null,
  official_or_community: t.official_or_community, live_vs_paper: t.live_vs_paper,
  safety_pct: t.safety_pct ?? null, safety_partial: t.safety_partial ?? null, safety_level: t.safety_level ?? null,
  url: t.url, details_url: t.details_url,
});

export function compare(tools, a, b) {
  const x = findTool(tools, a), y = findTool(tools, b);
  if (!x || !y) return { error: `Not found: ${[!x && a, !y && b].filter(Boolean).join(", ")}. Try search_tools.` };
  const fields = ["category", "assets_covered", "live_vs_paper", "order_approval_safety", "pricing_free_tier", "rate_limits",
    "official_or_community", "safety_pct", "safety_partial", "safety_level", "who_places_order", "source", "last_checked", "details_url"];
  return { tools: [x.name, y.name], comparison: Object.fromEntries(fields.map((f) => [f, { [x.name]: x[f] ?? null, [y.name]: y[f] ?? null }])) };
}
