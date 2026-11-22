#!/bin/bash
if [ -z "$BCKjNzpJ8LKLgBDLWrjFLJ66hqcnpRgMkKcJ8GNW" ]; then
  echo "Set USDA_API_KEY first"; exit 1
fi
curl -s "https://api.nal.usda.gov/fdc/v1/foods/search?query=chicken%20breast&pageSize=2&api_key=$BCKjNzpJ8LKLgBDLWrjFLJ66hqcnpRgMkKcJ8GNW" | jq .
