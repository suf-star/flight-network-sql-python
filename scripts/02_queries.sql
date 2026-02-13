-- 1) Top source airports by number of outgoing routes
SELECT a.Name, a.City, a.Country, COUNT(*) AS outgoing_routes
FROM routes r
JOIN airports a ON a.AirportID = r.SourceAirportID
WHERE r.SourceAirportID IS NOT NULL
GROUP BY a.AirportID
ORDER BY outgoing_routes DESC
LIMIT 15;

-- 2) Top destination airports by number of incoming routes
SELECT a.Name, a.City, a.Country, COUNT(*) AS incoming_routes
FROM routes r
JOIN airports a ON a.AirportID = r.DestAirportID
WHERE r.DestAirportID IS NOT NULL
GROUP BY a.AirportID
ORDER BY incoming_routes DESC
LIMIT 15;

-- 3) Airlines with most routes (by AirlineID)
SELECT al.Name, al.Country, COUNT(*) AS routes_count
FROM routes r
JOIN airlines al ON al.AirlineID = r.AirlineID
WHERE r.AirlineID IS NOT NULL
GROUP BY al.AirlineID
ORDER BY routes_count DESC
LIMIT 20;

-- 4) Countries with most airports
SELECT Country, COUNT(*) AS airports_count
FROM airports
GROUP BY Country
ORDER BY airports_count DESC
LIMIT 20;

-- 5) Most common route pairs (airport-to-airport), show names
SELECT
  src.Name AS source_airport,
  src.City AS source_city,
  src.Country AS source_country,
  dst.Name AS dest_airport,
  dst.City AS dest_city,
  dst.Country AS dest_country,
  COUNT(*) AS route_frequency
FROM routes r
JOIN airports src ON src.AirportID = r.SourceAirportID
JOIN airports dst ON dst.AirportID = r.DestAirportID
GROUP BY r.SourceAirportID, r.DestAirportID
ORDER BY route_frequency DESC
LIMIT 20;

-- 6) Average number of stops by airline (filter missing)
SELECT al.Name, AVG(r.Stops) AS avg_stops
FROM routes r
JOIN airlines al ON al.AirlineID = r.AirlineID
WHERE r.Stops IS NOT NULL
GROUP BY al.AirlineID
ORDER BY avg_stops DESC
LIMIT 20;

-- 7) Airports missing coordinates (data quality)
SELECT COUNT(*) AS airports_missing_coords
FROM airports
WHERE Latitude IS NULL OR Longitude IS NULL;

-- 8) Routes where source airport ID is missing (data quality)
SELECT COUNT(*) AS routes_missing_source_id
FROM routes
WHERE SourceAirportID IS NULL;

-- 9) Routes where destination airport ID is missing (data quality)
SELECT COUNT(*) AS routes_missing_dest_id
FROM routes
WHERE DestAirportID IS NULL;

-- 10) Active airlines vs inactive (rough indicator)
SELECT Active, COUNT(*) AS airline_count
FROM airlines
GROUP BY Active;

-- 11) Top cities by number of airports
SELECT City, Country, COUNT(*) AS airports_in_city
FROM airports
GROUP BY City, Country
ORDER BY airports_in_city DESC
LIMIT 20;

-- 12) Domestic vs international route count
SELECT
  CASE
    WHEN src.Country = dst.Country THEN 'Domestic'
    ELSE 'International'
  END AS route_type,
  COUNT(*) AS route_count
FROM routes r
JOIN airports src ON src.AirportID = r.SourceAirportID
JOIN airports dst ON dst.AirportID = r.DestAirportID
GROUP BY route_type;

