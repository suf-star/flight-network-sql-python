import sqlite3
import math
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

DB_PATH = "output/flights.sqlite"

def haversine_km(lat1, lon1, lat2, lon2):
    # Great-circle distance
    R = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dl/2)**2
    return 2 * R * math.asin(math.sqrt(a))

def main():
    conn = sqlite3.connect(DB_PATH)

    # Pull a joined dataset for modelling
    q = """
    SELECT
      r.AirlineID,
      src.Country AS src_country,
      dst.Country AS dst_country,
      src.Latitude AS src_lat,
      src.Longitude AS src_lon,
      dst.Latitude AS dst_lat,
      dst.Longitude AS dst_lon
    FROM routes r
    JOIN airports src ON src.AirportID = r.SourceAirportID
    JOIN airports dst ON dst.AirportID = r.DestAirportID
    WHERE src.Latitude IS NOT NULL AND src.Longitude IS NOT NULL
      AND dst.Latitude IS NOT NULL AND dst.Longitude IS NOT NULL;
    """
    df = pd.read_sql_query(q, conn)
    conn.close()

    # Feature engineering
    df["distance_km"] = df.apply(
        lambda x: haversine_km(x["src_lat"], x["src_lon"], x["dst_lat"], x["dst_lon"]),
        axis=1
    )
    df["is_international"] = (df["src_country"] != df["dst_country"]).astype(int)

    # Simple chart: distribution of route distance
    plt.figure()
    df["distance_km"].clip(upper=6000).plot(kind="hist", bins=50)
    plt.xlabel("Route distance (km) (clipped at 6000)")
    plt.ylabel("Count")
    plt.title("Distribution of route distances")
    plt.tight_layout()
    plt.savefig("output/distance_distribution.png", dpi=200)

    # Chart: domestic vs international counts
    plt.figure()
    df["is_international"].value_counts().sort_index().plot(kind="bar")
    plt.xticks([0, 1], ["Domestic", "International"], rotation=0)
    plt.ylabel("Number of routes")
    plt.title("Domestic vs International routes")
    plt.tight_layout()
    plt.savefig("output/domestic_vs_international.png", dpi=200)

    # Tiny model: predict international from distance only (baseline)
    X = df[["distance_km"]]
    y = df["is_international"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = LogisticRegression(max_iter=200)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    acc = accuracy_score(y_test, preds)

    with open("output/model_results.txt", "w", encoding="utf-8") as f:
        f.write(f"Accuracy: {acc:.4f}\n\n")
        f.write(classification_report(y_test, preds))

    print("✅ Analysis complete.")
    print("Saved charts to output/*.png and model results to output/model_results.txt")

if __name__ == "__main__":
    main()
