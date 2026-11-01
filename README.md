# Food Tracker

A simple command-line tool that looks up common foods and tells you how much protein, carbohydrates, and fat are in what you ate.

## The Problem

Tracking what you eat each day is useful, especially in college, but popular nutrition apps hide basic features behind subscriptions, show ads, and take many steps to log a single food. I wanted something much simpler. I simply want to pick a food, enter roughly how much I ate, and instantly see the nutrients and my total for the day.

## How It Works

You run the program and type a food name. It searches the [USDA FoodData Central](https://fdc.nal.usda.gov/) API, shows the closest matches, and asks how many grams you ate. It scales the per-100 g nutrient values to your amount, prints the calories, protein, carbs, and fat, and saves the entry to a local `log.json` file. A second script reads that file with `jq` and prints your totals for the day, and can optionally run every night with `cron`.

## Tech Stack

- **Language:** Python 3 (main program), Bash (helper scripts)
- **Libraries:** `requests` (API calls), plus the built-in `json` and `datetime` modules
- **External tools:** `curl` and `jq` (Bash scripts), `cron` (optional scheduling)
- **External API:** USDA FoodData Central (free API key required)
- **Storage:** a local JSON file, `data/log.json`

## Setup

1. Clone the repo and enter it:

   ```bash
   git clone https://github.com/nikhilprashanth/food-tracker.git
   cd food-tracker
   ```

2. Install the dependencies (you need Python 3 and `jq` installed):

   ```bash
   pip install requests
   ```

3. Get a free API key at <https://fdc.nal.usda.gov/api-key-signup.html>, then set it in your terminal:

   ```bash
   export USDA_API_KEY=your_key_here
   ```

4. Make the scripts executable:

   ```bash
   chmod +x run.sh scripts/*.sh
   ```

## Usage

Start the program:

```bash
./run.sh
```

Example session:

```
Food: chicken breast
1) Chicken breast, cooked
2) Chicken breast, raw
Pick a match: 1
Grams: 150

Calories: 248   Protein: 46.5 g   Carbs: 0 g   Fat: 5.4 g
Saved to data/log.json
```

Print today's totals from the saved log:

```bash
./scripts/today.sh
```

Test that your API key works (prints the raw JSON response):

```bash
./scripts/test_api.sh
```

Optional: print your totals every night at 9 pm by adding this line with `crontab -e`:

```
0 21 * * * /full/path/to/food-tracker/scripts/today.sh
```

## Project Structure

```
food-tracker/
├── README.md
├── run.sh                 # entry point
├── src/tracker.py         # main program
├── scripts/
│   ├── today.sh           # daily totals via jq
│   └── test_api.sh        # curl test of the USDA API
├── Eisenhower_Matrix.pdf # Eisenhower Matrix
├── Schematic_Diagram.png  # System Diagram
└── data/                  # log.json is created here
```

## Roadmap

Features I haven't built yet but plan to:

- [ ] Design a good user interface
- [ ] Allow users to enter multiple food items for each meal
- [ ] Improve error handling features, and missing data for particular foods
- [ ] Add a food intake summary per day

## Author

Nikhil Prashanth — [GitHub profile](https://github.com/nikhilprashanth)
