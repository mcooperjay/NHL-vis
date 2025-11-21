import pandas as pd

df = pd.read_csv("nhl_player_expanded.csv")

cols = ["A","EVG","EVP","FOW%","GWG","GP","G","lastName","OTG","PIM","playerId","+/-",
        "P","P/GP","Pos","PPG","PPP","Season","SHG","SHP","S%","S/C","S","Player","Team","TOI/GP"]

df.columns = cols

df["Season"] = df["Season"].astype(str).str.extract(r"(.{4}).{4}").astype(int)



df.to_csv("nhl_players_cleaned.csv")