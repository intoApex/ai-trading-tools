import { copyFileSync, mkdirSync } from "node:fs";
mkdirSync(new URL("../data/", import.meta.url), { recursive: true });
copyFileSync(new URL("../../data/tools.json", import.meta.url), new URL("../data/tools.json", import.meta.url));
