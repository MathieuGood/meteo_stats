import pandas as pd


def main():
    print("Hello from climate-stats!")

    df1 = pd.read_csv("Q_67_latest-2024-2025_RR-T-Vent.csv", sep=";")
    def2 = pd.read_csv("Q_67_latest-2024-2025_RR-T-Vent.csv", sep=";")

    df = pd.concat([df1, def2], ignore_index=True)

    # Filter only NOM_USUEL that has  'STRASBOURG' in it
    df = df[df["NOM_USUEL"].str.contains("STRASBOURG-ENTZHEIM", case=False, na=False)]

    # Print a graph with each average temperature in August for each year
    df["ANNEE"] = pd.to_datetime(df["AAAAMMJJ"]).dt.year
    df["MOIS"] = pd.to_datetime(df["AAAAMMJJ"]).dt.month
    print(df)
    df_august = df[df["MOIS"] == 8]
    print(df_august)
    df_avg_august = df_august.groupby("ANNEE")["TX"].mean().reset_index()
    df_avg_august.columns = ["ANNEE", "AVG_TX_AUGUST"]
    print(df_avg_august)
    df_avg_august["AVG_TX_AUGUST"] = df_avg_august["AVG_TX_AUGUST"].round(2)
    df_avg_august = df_avg_august.sort_values(by="ANNEE")
    df_avg_august.reset_index(drop=True, inplace=True)
    print("Average temperatures in August for each year:")
    print(df_avg_august)


if __name__ == "__main__":
    main()
