# Flight network analysis (SQL + Python)

## What this is
A small end-to-end project demonstrating **SQLite + SQL querying + Python analysis/visualisation + a tiny baseline model**, using the OpenFlights dataset (airports, airlines, routes).

## Project structure
- `data/` — raw OpenFlights files (`airports.dat`, `airlines.dat`, `routes.dat`)
- `scripts/01_load_to_sqlite.py` — loads data into SQLite (`output/flights.sqlite`)
- `scripts/02_queries.sql` — SQL queries (joins, GROUP BY, CASE, data quality checks)
- `scripts/03_analysis_and_model.py` — charts + baseline model
- `output/` — database + results (PNG charts, model metrics, SQL results)

## How to run (from the project root)
1) Create / rebuild the SQLite database  
   Run: `python scripts/01_load_to_sqlite.py`

2) Generate charts + baseline model metrics  
   Run: `python scripts/03_analysis_and_model.py`

3) Run SQL queries (optional, if you want to regenerate results)  
   Execute the statements in `scripts/02_queries.sql` against `output/flights.sqlite` and save outputs to `output/sql_results.txt`.

## Outputs
- `output/flights.sqlite`
- `output/sql_results.txt`
- `output/distance_distribution.png`
- `output/domestic_vs_international.png`
- `output/model_results.txt` (accuracy ~0.7039)

## Key findings (from SQL)
- **Top hub airports (outgoing routes):** Atlanta (915), Chicago O’Hare (558), Beijing (535), London Heathrow (527), Paris CDG (524).
- **Airports by country:** United States (1512), Canada (430), Australia (334), Russia (264), Brazil (264).
- **Airlines by route count:** Ryanair (2484), American (2354), United (2180), Delta (1981), easyJet (1130).
- **Route mix:** International (34710) slightly exceeds Domestic (32061).
- **Data quality:** 0 airports missing coordinates; ~220 routes have missing source/destination airport IDs.

## Baseline model
Logistic Regression predicts **international vs domestic** routes using **distance only**.
- Test accuracy: ~0.7039 (see `output/model_results.txt`)
- Interpretation: distance is informative, but overlap (short international / long domestic) limits performance.

## Next steps
- Add features (airline, hub score, route frequency, region/continent) and compare models.
- Build a small dashboard (e.g., Streamlit) to explore hubs and routes interactively.

