import json
import os
import sys
from datetime import date

import requests

API_KEY = os.environ.get("USDA_API_KEY")
URL = "https://api.nal.usda.gov/fdc/v1/foods/search"
LOG_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "log.json")

NUTRIENT_IDS = {"calories": 1008, "protein": 1003, "carbs": 1005, "fat": 1004}


def search_foods(query):
    resp = requests.get(
        URL,
        params={
            "query": query,
            "api_key": API_KEY,
            "pageSize": 5,
            "dataType": "Foundation,SR Legacy",  # values are per 100 g
        },
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json().get("foods", [])


def per_100g(food):
    values = {name: 0.0 for name in NUTRIENT_IDS}
    for n in food.get("foodNutrients", []):
        for name, nid in NUTRIENT_IDS.items():
            if n.get("nutrientId") == nid:
                values[name] = n.get("value", 0)
    return values



def scale(values, grams):
    return {k: round(v * grams / 100, 1) for k, v in values.items()}


def save_entry(entry):
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    try:
        with open(LOG_PATH) as f:
            log = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        log = []
    log.append(entry)
    with open(LOG_PATH, "w") as f:
        json.dump(log, f, indent=2)


def main():
    if not API_KEY:
        sys.exit("Set the USDA_API_KEY environment variable first.")

    query = input("Food: ").strip()
    try:
        foods = search_foods(query)
    except requests.RequestException as e:
        sys.exit(f"API error: {e}")

    if not foods:
        sys.exit("No matches found.")

    for i, food in enumerate(foods, 1):
        print(f"{i}) {food['description']}")

    try:
        choice = int(input("Pick a match: ")) - 1
        grams = float(input("Grams: "))
        food = foods[choice]
    except (ValueError, IndexError):
        sys.exit("Invalid input.")

    result = scale(per_100g(food), grams)
    print(
        f"\nCalories: {result['calories']:.0f}   Protein: {result['protein']} g   "
        f"Carbs: {result['carbs']} g   Fat: {result['fat']} g"
    )

    save_entry({
        "date": date.today().isoformat(),
        "food": food["description"],
        "grams": grams,
        **result,
    })
    print("Saved to data/log.json")


if __name__ == "__main__":
    main()
