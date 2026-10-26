import { test } from "node:test";
import assert from "node:assert/strict";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

test("server lists and runs all tools over stdio", async () => {
  const client = new Client({ name: "smoke", version: "0" });
  await client.connect(new StdioClientTransport({ command: process.execPath, args: [new URL("../src/index.js", import.meta.url).pathname] }));
  const names = (await client.listTools()).tools.map((t) => t.name).sort();
  assert.deepEqual(names, ["compare_brokers", "get_tool", "list_categories", "search_tools"]);
  const parse = (r) => JSON.parse(r.content[0].text);
  const cats = parse(await client.callTool({ name: "list_categories", arguments: {} }));
  assert.equal(cats.reduce((s, c) => s + c.count, 0) > 30, true);
  const s = parse(await client.callTool({ name: "search_tools", arguments: { query: "alpaca", category: "broker_mcp" } }));
  assert.equal(s.results[0].slug, "alpaca-mcp-server");
  const g = parse(await client.callTool({ name: "get_tool", arguments: { slug: "alpaca-mcp-server" } }));
  assert.match(g.order_approval_safety, /ALPACA_TOOLSETS/);
  assert.equal(typeof g.safety_pct, "number");
  const c = parse(await client.callTool({ name: "compare_brokers", arguments: { a: "alpaca-mcp-server", b: "tradier-mcp-server" } }));
  assert.deepEqual(c.tools, ["Alpaca MCP Server", "Tradier MCP Server"]);
  const miss = await client.callTool({ name: "get_tool", arguments: { slug: "zzzz-nope" } });
  assert.equal(miss.isError, true);
  console.log(`OK: ${names.length} tools; ${cats.length} categories; search 'alpaca' -> ${s.results.map((r) => r.slug).join(", ")}`);
  await client.close();
});
