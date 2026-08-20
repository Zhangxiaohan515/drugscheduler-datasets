import fs from "node:fs/promises";
import path from "node:path";
import { pathToFileURL } from "node:url";

const [csvPathArg, outPathArg] = process.argv.slice(2);

if (!csvPathArg || !outPathArg) {
  console.error("Usage: node export_review_table_xlsx.mjs <review_table.csv> <review_table.xlsx>");
  process.exit(2);
}

const nodeModules = process.env.CODEX_ARTIFACT_NODE_MODULES;
if (!nodeModules) {
  console.error("CODEX_ARTIFACT_NODE_MODULES must point to the bundled node_modules directory.");
  process.exit(2);
}

const artifactToolUrl = pathToFileURL(
  path.join(nodeModules, "@oai", "artifact-tool", "dist", "artifact_tool.mjs"),
).href;
const { SpreadsheetFile, Workbook } = await import(artifactToolUrl);

const csvPath = path.resolve(csvPathArg);
const outPath = path.resolve(outPathArg);
const csvText = await fs.readFile(csvPath, "utf8");
const workbook = await Workbook.fromCSV(csvText, { sheetName: "review_table_rules" });
const sheet = workbook.worksheets.getItem("review_table_rules");

sheet.showGridLines = false;
sheet.freezePanes.freezeRows(1);

const usedRange = sheet.getUsedRange();
usedRange.format = {
  font: { name: "Aptos", size: 10 },
  wrapText: true,
};

sheet.getRange("A1:Q1").format = {
  fill: "#1F4E78",
  font: { bold: true, color: "#FFFFFF" },
  wrapText: true,
};
sheet.getRange("A1:Q1").format.borders = {
  preset: "bottom",
  style: "medium",
  color: "#BFBFBF",
};

const widths = {
  A: 22,
  B: 16,
  C: 24,
  D: 14,
  E: 24,
  F: 14,
  G: 24,
  H: 12,
  I: 12,
  J: 14,
  K: 60,
  L: 45,
  M: 22,
  N: 18,
  O: 36,
  P: 20,
  Q: 28,
};

for (const [column, width] of Object.entries(widths)) {
  sheet.getRange(`${column}:${column}`).format.columnWidth = width;
}
sheet.getRange("A:Q").format.verticalAlignment = "top";

const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(outPath);

const previewPath = outPath.replace(/\.xlsx$/i, "_preview.png");
const preview = await workbook.render({
  sheetName: "review_table_rules",
  range: "A1:O12",
  scale: 1,
  format: "png",
});
await fs.writeFile(previewPath, new Uint8Array(await preview.arrayBuffer()));

const inspect = await workbook.inspect({
  kind: "sheet,region",
  sheetId: "review_table_rules",
  range: "A1:O8",
  maxChars: 2000,
});
const errors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 100 },
  summary: "formula error scan",
});

console.log(JSON.stringify({
  xlsx: outPath,
  preview: previewPath,
  inspect: inspect.ndjson,
  formula_error_scan: errors.ndjson,
}, null, 2));
