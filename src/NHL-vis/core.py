import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from typing import List


df = pd.read_csv("nhl_player_expanded.csv")


def get_player_stats(name: str, season=None, aggr=True):
    """
    Creates a dataframe for an NHL player's stats.
    """

    # Filter by player name
    player_df = df[df["Player"] == name].copy()

    if player_df.empty:
        return pd.DataFrame()

    # --- Fix: normalize season input ---
    if season is None:
        season_list = None
    elif isinstance(season, list):
        season_list = season
    else:
        season_list = [season]

    # Filter by season(s)
    if season_list is not None:
        player_df = player_df[player_df["Season"].isin(season_list)]

    if not aggr:
        return player_df

    # --- Aggregate block ---
    start_season = player_df["Season"].min()
    end_season   = player_df["Season"].max()
    seasons = f"{start_season}-{end_season}"

    player = player_df["Player"].iloc[0]

    # Unique-string helpers
    teams = ",".join(sorted(player_df["Team"].unique()))
    sc    = ",".join(sorted(player_df["S/C"].unique()))
    pos   = ",".join(sorted(player_df["Pos"].unique()))

    gp = player_df["GP"].sum()
    g  = player_df["G"].sum()
    a  = player_df["A"].sum()
    p  = player_df["P"].sum()

    plusminus = player_df["+/-"].sum()
    pim       = player_df["PIM"].sum()

    p_gp = p / gp if gp > 0 else None

    evg = player_df["EVG"].sum()
    evp = player_df["EVP"].sum()
    ppg = player_df["PPG"].sum()
    ppp = player_df["PPP"].sum()
    shg = player_df["SHG"].sum()
    shp = player_df["SHP"].sum()
    otg = player_df["OTG"].sum()
    gwg = player_df["GWG"].sum()

    s = player_df["S"].sum()
    sp = g / s if s > 0 else None

    TOI = player_df["TOI/GP"].mean()
    FOW = player_df["FOW%"].mean()

    # --- Build final one-row dataframe ---
    result = pd.DataFrame([{
        "Player": player,
        "Season(s)": seasons,
        "Team(s)": teams,
        "S/C": sc,
        "Position": pos,
        "GP": gp,
        "S": s,
        "G": g,
        "A": a,
        "P": p,
        "S%": sp,
        "+/-": plusminus,
        "PIM": pim,
        "P/GP": p_gp,
        "EVG": evg,
        "EVP": evp,
        "PPG": ppg,
        "PPP": ppp,
        "SHG": shg,
        "SHP": shp,
        "OTG": otg,
        "GWG": gwg,
        "TOI/GP": TOI,
        "FOW%": FOW
    }])

    return result

    

def get_roster_stats(team, season):
    """
    Returns the roster and stats of a team for a given season.

    Inputs:
        Team: Three letter abbreviation (as used on NHL.com)
        Season: Integer of the first year a season begins.
    """

    data = df.copy()
    data = data[data["Team"].str.contains(team, case=False, regex=False)]
    data = data[data["Season"]==season]

    return data

def score_plot(player, season=2024, metrics=["P", "G", "A"]):
    """
    Plots a player's goals, assists, and points relative to the league averages.

    Other metrics can be included as a list in the metrics argument.

    Inputs:
        Player: Player name
        Season: Integer of the first year a season begins.
        Metrics: List containing any available metrics.
    """

    dfc = df[df["Season"]==season].copy()

    playerd = dfc[dfc["Player"]==player].copy()
    if playerd.empty:
        print("No data found for this player!")
        return
    
    league_avg = dfc[metrics].mean()

    plot_rows = []

    for m in metrics:
        plot_rows.append({"Metric": m, "Value": playerd.iloc[0][m], "Type": "Player"})
        plot_rows.append({"Metric": m, "Value": league_avg[m], "Type": "League Average"})

    plotdf = pd.DataFrame(plot_rows)

    fig = px.bar(
        plotdf,
        x="Metric",
        y="Value",
        color="Type",
        barmode="group",
        text="Value",
        title=f"{player} vs League Averages ({season})"
    )

    fig.show()


# TODO: Filter data before so it's more meaningful? 
def score_scatter(player=None, season=None, team=None, metrics=["G", "A"]):

    if season is not None:
        data = df[df["Season"]==season].copy()
    else:
        data = df.copy()
    def make_highlights(x, y):
        if (x == player and y == team):
            return f"{player} / {team}"
        elif x == player:
            return player
        elif y == team:
            return team
        else:
            return "Other"
        
    data["highlight"] = data.apply(
        lambda row: make_highlights(row["Player"], row["Team"]),
        axis=1
    )

    fig = px.scatter(
        data, x=metrics[0], y=metrics[1],
        color="highlight", hover_name="Player",
        hover_data = ["Team", "G", "A", "P", "S/C", "Pos", "GP", "GWG", "S%"],
        title=f"NHL {metrics[0]} and {metrics[1]}"
    )
    fig.show()



score_scatter(player= "Connor McDavid", team="EDM", metrics=["S%", "G"])
score_plot("Connor McDavid", 20242025)

# TODO: Fix seasons in the csv.