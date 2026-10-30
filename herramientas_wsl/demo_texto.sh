#!/usr/bin/env bash
mkdir -p /tmp/demo
curl -s "https://es.wikisource.org/w/api.php?action=query&prop=extracts&explaintext=1&titles=El_criterio/01&format=json" \
  | jq -r '.query.pages[].extract' > /tmp/demo/balmes01.txt
wc -w /tmp/demo/balmes01.txt
cat /tmp/demo/balmes01.txt
