import sqlite3
import pandas as pd

DB_PATH = "output/flights.sqlite"

AIRPORT_COLS = [
    "AirportID","Name","City","Country","IATA","ICAO",
    "Latitude","Longitude","Altitude","Timezone","DST","TzDatabase",
    "Type","Source"
]

AIRLINE_COLS = [
    "AirlineID","Name","Alias","IATA","ICAO","Callsign","Country","Active"
]

ROUTE_COLS = [
    "Airline","AirlineID","SourceAirport","SourceAirportID",
    "DestAirport","DestAirportID","Codeshare","Stops","Equipment"
]

def read_openflights(path: str, cols: list[str]) -> pd.DataFrame:
    # OpenFlights uses \N for missing values
    return pd.read_csv(
        path,
        header=None,
        names=cols,
        na_values="\\N",
        encoding="utf-8",
    )

def main():
    airports = read_openflights("data/airports.dat", AIRPORT_COLS)
    airlines = read_openflights("data/airlines.dat", AIRLINE_COLS)
    routes = read_openflights("data/routes.dat", ROUTE_COLS)

    # Clean some obvious types
    for c in ["AirportID"]:
        airports[c] = pd.to_numeric(airports[c], errors="coerce")
    for c in ["Latitude","Longitude"]:
        airports[c] = pd.to_numeric(airports[c], errors="coerce")

    routes["Stops"] = pd.to_numeric(routes["Stops"], errors="coerce")
    routes["SourceAirportID"] = pd.to_numeric(routes["SourceAirportID"], errors="coerce")
    routes["DestAirportID"] = pd.to_numeric(routes["DestAirportID"], errors="coerce")
    airlines["AirlineID"] = pd.to_numeric(airlines["AirlineID"], errors="coerce")

    conn = sqlite3.connect(DB_PATH)

    airports.to_sql("airports", conn, if_exists="replace", index=False)
    airlines.to_sql("airlines", conn, if_exists="replace", index=False)
    routes.to_sql("routes", conn, if_exists="replace", index=False)

    # Helpful indexes for joins
    conn.execute("CREATE INDEX IF NOT EXISTS idx_airports_id ON airports(AirportID)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_airlines_id ON airlines(AirlineID)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_routes_srcid ON routes(SourceAirportID)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_routes_dstid ON routes(DestAirportID)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_routes_airlineid ON routes(AirlineID)")

    conn.commit()
    conn.close()

    print(f"✅ Database created at {DB_PATH}")
    print(f"Airports: {len(airports):,} | Airlines: {len(airlines):,} | Routes: {len(routes):,}")

if __name__ == "__main__":
    main()
