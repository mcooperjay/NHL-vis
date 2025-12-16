import pandas as pd
import matplotlib.pyplot as plt


TEAM_ABBREV = "UTA"   # Utah Mammoth / Utah Hockey Club


def run_analysis_pipeline():
    print("Running analysis pipeline...")
    #Loading the data
    df = pd.read_csv("src/nhl_vis_386/nhl_players_cleaned.csv")
    gaps = compute_team_gaps(df, "UTA" )
    #Team v League
    fig = plot_team_gaps(gaps)
    fig.savefig("mammoth_gaps.png", dpi=300, bbox_inches="tight")
    #Separated by Forwards and Defensevemen
    #Forwards
    forward_gaps = compute_all_forward_gaps(df, "UTA")
    fig = plot_all_forward_gaps(forward_gaps)
    fig.savefig("forwards_mammoth_gaps.png", dpi=300)
    # Forwards  and Defense (separated)
    for pos in ["C", "L", "R"]:
      print(f"Running for Position: {pos}")
      gaps = compute_forward_position_gaps(df, "UTA", pos)
      fig = plot_forward_position_gaps(gaps, pos)
      fig.savefig(f"{pos}_mammoth_gaps.png", dpi=300)
    #Scatterplot of Forwards
    fig = scatter_metric_by_position(df, "UTA", "F", "TOI/GP", "P/GP")
    fig.savefig("scatter_F_TOI_PGP.png", dpi=300)

    print("All analyses complete!")
    print("Outputs written to current directory.")

def compute_team_gaps(df, team_abbrev):
    metrics = ["G", "A", "P", "S", "PIM", "+/-", "FOW%", "S%"]

    team = df[df["Team"] == team_abbrev]
    league = df

    df_out = pd.DataFrame({
        "team_median": team[metrics].median(),
        "league_median": league[metrics].median(),
    })

    df_out["gap"] = df_out["team_median"] - df_out["league_median"]
    return df_out

def plot_team_gaps(gaps):
    fig, ax = plt.subplots(figsize=(8, 5))

    ax.bar(gaps.index, gaps["gap"])
    ax.set_title("Utah Mammoth vs League Median")
    ax.set_ylabel("League median - Mammoth median")
    ax.tick_params(axis="x", rotation=45)
    ax.axhline(0, linestyle="--")

    fig.tight_layout()
    return fig

def compute_team_gaps_pos(df, team_abbrev, position):
    metrics = ["G", "A", "P", "S", "PIM", "+/-", "FOW%", "S%"]

    results = []

    if position == "F":
        positions = ["C", "L", "R"]
    else:
        positions = [position]

    for pos in positions:
        df_pos = df[df["Pos"] == pos]

        team = df_pos[df_pos["Team"] == team_abbrev]
        league = df_pos

        for metric in metrics:
          results.append({
            "metric": metric, 
            "position": pos, 
            "gap":team[metric].median() - league[metric].median()
          })
    return pd.DataFrame(results)

def plot_position_gaps(gaps, position):
    fig, ax = plt.subplots(figsize=(8, 5))

    labels = [f"{pos}-{metric}" for pos, metric in zip(gaps["position"], gaps.index)]

    ax.bar(labels, gaps["gap"])
    ax.axhline(0, linestyle="--")

    ax.set_title(f"Utah Mammoth vs League Median ({position})")
    ax.set_ylabel("League median − Mammoth median")
    ax.tick_params(axis="x", rotation=45)

    fig.tight_layout()
    return fig

def scatter_metric_by_position(df, team_abbrev, position, x, y):
    df_pos = df[df["Pos"] == position]

    fig, ax = plt.subplots(figsize=(7, 6))

    if position == "F":
        df_pos = df[df["Pos"].isin(["C", "L", "R"])]
    else:
        df_pos = df[df["Pos"] == position]

    # Safety check
    if df_pos.empty:
        raise ValueError(f"No data found for position '{position}'")


    league = df_pos[df_pos["Team"] != team_abbrev]
    team = df_pos[df_pos["Team"] == team_abbrev]

    ax.scatter(league[x], league[y], alpha=0.3, label="League")
    ax.scatter(team[x], team[y], color="red", label="Utah")

    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.set_title(f"{position}: {y} vs {x}")
    ax.legend()

    fig.tight_layout()
    return fig

def compute_all_forward_gaps(df, team_abbrev):
    metrics = ["G", "A", "P", "S", "PIM", "+/-", "FOW%", "S%"]

    df_forwards = df[df["Pos"].isin(["C", "L", "R"])]

    team = df_forwards[df_forwards["Team"] == team_abbrev]
    league = df_forwards

    gaps = {
        metric: team[metric].median() - league[metric].median()
        for metric in metrics
    }

    return pd.DataFrame({
        "metric": gaps.keys(),
        "gap": gaps.values()
    })

def plot_all_forward_gaps(gaps):
    fig, ax = plt.subplots(figsize=(8, 5))

    ax.bar(gaps["metric"], gaps["gap"])
    ax.axhline(0, linestyle="--")

    ax.set_title("Utah Mammoth vs League Median — All Forwards")
    ax.set_ylabel("League median − Mammoth median")
    ax.tick_params(axis="x", rotation=45)

    fig.tight_layout()
    return fig

def compute_forward_position_gaps(df, team_abbrev, position):
    metrics = ["G", "A", "P", "S", "PIM", "+/-", "FOW%", "S%"]

    df_pos = df[df["Pos"] == position]

    team = df_pos[df_pos["Team"] == team_abbrev]
    league = df_pos

    gaps = {
        metric: team[metric].median() - league[metric].median()
        for metric in metrics
    }

    return pd.DataFrame({
        "metric": gaps.keys(),
        "gap": gaps.values()
    })

def plot_forward_position_gaps(gaps, position):
    fig, ax = plt.subplots(figsize=(8, 5))

    ax.bar(gaps["metric"], gaps["gap"])
    ax.axhline(0, linestyle="--")

    ax.set_title(f"Utah Mammoth vs League Median — {position}")
    ax.set_ylabel("League median − Mammoth median")
    ax.tick_params(axis="x", rotation=45)

    fig.tight_layout()
    return fig

if __name__ == "__main__":
    run_analysis_pipeline()
