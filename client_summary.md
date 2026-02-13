# Client summary — Flight network analysis (OpenFlights)

## What I built
- Loaded OpenFlights (airports, airlines, routes) into a SQLite database (`output/flights.sqlite`)
- Wrote SQL queries (`scripts/02_queries.sql`) to answer hub/airline/country + data-quality questions
- Built a Python analysis script that engineers route distance, produces charts, and trains a baseline model

## Outputs
- `output/distance_distribution.png`
- `output/domestic_vs_international.png`
- `output/model_results.txt` (accuracy ~0.7039)
- `output/sql_results.txt`

## Key findings
- **Top hubs (outgoing routes):** Atlanta (915), Chicago O’Hare (558), Beijing (535), Heathrow (527), Paris CDG (524)
- **Airports by country:** United States (1512) leads, then Canada (430), Australia (334)
- **Airlines by route count:** Ryanair (2484) leads; American (2354), United (2180), Delta (1981), easyJet (1130)
- **Route mix:** International (34710) slightly exceeds Domestic (32061)
- **Data quality:** 0 airports missing coordinates; ~220 routes have missing source/destination airport IDs

## Baseline model
- Logistic Regression predicts **international vs domestic** using **distance only**
- Test accuracy: **~0.7039**
- Takeaway: distance helps, but overlap (short international / long domestic) limits performance
