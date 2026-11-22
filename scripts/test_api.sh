#!/bin/bash
if [ -z "$USDA_API_KEY" ]; then
  echo "Set USDA_API_KEY first"; exit 1
fi
curl -s "https://api.nal.usda.gov/fdc/v1/foods/search?query=chicken%20breast&pageSize=2&api_key=$USDA_API_KEY" | jq .
