import polars as pl
import matplotlib.pyplot as plt

# Read the CSV files and concatenate them
df1 = pl.read_csv("Q_67_previous-1950-2023_RR-T-Vent.csv", separator=";")
df2 = pl.read_csv("Q_67_latest-2024-2025_RR-T-Vent.csv", separator=";")
df = pl.concat([df1, df2])

# Only keep relevant columns
df = df.select(["NOM_USUEL", "TX", "AAAAMMJJ"])
# Convert to datetime and add columns for year and month
df = df.with_columns([
    pl.col("AAAAMMJJ").str.strptime(pl.Date, "%Y%m%d", strict=False).alias("AAAAMMJJ"),
])
df = df.with_columns([
    pl.col("AAAAMMJJ").dt.year().alias("ANNEE"),
    pl.col("AAAAMMJJ").dt.month().alias("MOIS")
])

# Print all USUAL_NAME values alphabetically
unique_names = df.select("NOM_USUEL").unique().sort("NOM_USUEL")
print(unique_names)

# Filter by station name STRASBOURG-ENTZHEIM, STRASBOURG - BOTANIQUE and STRASBOURG - ZIEGELAU
df = df.filter(pl.col("NOM_USUEL").str.contains("STRASBOURG", case=False))

# Only keep data for the month of August for every year
df_august = df.filter(pl.col("MOIS") == 8)
# Only keep data from 1980 onwards
df_august = df_august.filter(pl.col("ANNEE") >= 1980)
# Group by year and calculate the mean TX
df_august = df_august.groupby("ANNEE").agg(pl.col("TX").mean().alias("TX"))

# Draw a graph of the mean TX over the years
plt.figure(figsize=(10, 5))
plt.plot(df_august["ANNEE"].to_numpy(), df_august["TX"].to_numpy(), marker='o')
plt.title("Mean Temperature in August at Strasbourg-Entzheim")
plt.xlabel("Year")
plt.ylabel("Mean Temperature (°C)")
plt.grid()
plt.xticks(df_august["ANNEE"].to_numpy(), rotation=45)
plt.tight_layout()
plt.show()

# Group by day and keep only the maximum and minimum temperature for each day
df_daily_max = df.groupby("AAAAMMJJ").agg(pl.col("TX").max().alias("TX"))
df_daily_min = df.groupby("AAAAMMJJ").agg(pl.col("TX").min().alias("TX"))

# Filter for hot temperatures above 38°C
max_temp = float(input("Enter the maximum temperature threshold (°C): "))
df_hot_temps = df_daily_max.filter(pl.col("TX") >= max_temp).sort("AAAAMMJJ")
print(f"{df_hot_temps.shape[0]} days with temperatures above {max_temp}°C")
print(df_hot_temps)
