#!/bin/bash

# File names
URL="https://www.amfiindia.com/spages/NAVAll.txt"
RAW_FILE="NAVAll.txt"
TSV_FILE="nav_data.tsv"
JSON_FILE="nav_data.json"

# Step 1: Download data
curl -s "$URL" -o "$RAW_FILE"

# Step 2: Filter lines with valid NAV data (skip headers and footers)
awk -F';' 'NF >= 6 && $1 ~ /^[0-9]+$/ { print $4 "\t" $5 }' "$RAW_FILE" > "$TSV_FILE"

echo "✅ Extracted data to $TSV_FILE"

# Step 3: (Optional) Convert to JSON
# Only use if jq is available
if command -v jq &>/dev/null; then
  echo "[" > "$JSON_FILE"
  awk -F'\t' '{ printf "{\"Scheme Name\": \"%s\", \"Asset Value\": \"%s\"},\n", $1, $2 }' "$TSV_FILE" \
    | sed '$ s/},/}/' >> "$JSON_FILE"
  echo "]" >> "$JSON_FILE"
  echo "✅ Converted TSV to $JSON_FILE"
fi
