#!/usr/bin/env node
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { CATEGORIES, loadTools, searchTools, findTool, summary, compare } from "./data.js";

const tools = await loadTools();
const json = (o) => ({ content: [{ type: "text", text: JSON.stringify(o, null, 2) }] });
const NOTE = "Data: TradingAgentStack (tradingagentstack.com), CC BY 4.0. Not financial advice; verify with each vendor.";
const ro = { readOnlyHint: true, openWorldHint: false };

const server = new McpServer({ name: "tradingagentstack", version: "0.1.0" });

server.registerTool("search_tools", {
  title: "Search AI trading tools",
  description: "Search the TradingAgentStack directory of broker MCP servers, broker/market-data APIs, agent frameworks, backtesters and security tools. Returns short summaries; use get_tool for full details.",
  inputSchema: { query: z.string().default("").describe("Keywords, e.g. 'options paper trading' or 'crypto'"),
    category: z.enum(Object.keys(CATEGORIES)).optional().describe("Optional category filter (see list_categories)"),
    limit: z.number().int().min(1).max(50).default(10) },
  annotations: ro,
}, async ({ query, category, limit }) => {
  const r = searchTools(tools, query, category);
  return json({ total: r.length, results: r.slice(0, limit).map(summary), note: NOTE });
});

server.registerTool("get_tool", {
  title: "Get tool details",
  description: "Full sourced record for one tool: assets, live vs paper, order approval/safety controls, pricing, rate limits, source and last-checked date.",
  inputSchema: { slug: z.string().describe("Tool slug or name, e.g. 'alpaca-mcp-server'") },
  annotations: ro,
}, async ({ slug }) => {
  const t = findTool(tools, slug);
  return t ? json({ ...t, note: NOTE }) : { isError: true, content: [{ type: "text", text: `No tool matching '${slug}'. Try search_tools.` }] };
});

server.registerTool("compare_brokers", {
  title: "Compare two tools",
  description: "Side-by-side comparison of two brokers/tools (safety controls, paper trading, pricing, rate limits).",
  inputSchema: { a: z.string().describe("First tool slug or name"), b: z.string().describe("Second tool slug or name") },
  annotations: ro,
}, async ({ a, b }) => {
  const r = compare(tools, a, b);
  return r.error ? { isError: true, content: [{ type: "text", text: r.error }] } : json({ ...r, note: NOTE });
});

server.registerTool("list_categories", {
  title: "List categories",
  description: "List directory categories with tool counts.",
  inputSchema: {},
  annotations: ro,
}, async () => json(Object.entries(CATEGORIES).map(([id, name]) => ({ id, name, count: tools.filter((t) => t.category === id).length }))));

await server.connect(new StdioServerTransport());
