import pandas as pd
import matplotlib.pyplot as plt


TEAM_ABBREV = "UTA"   # Utah Mammoth / Utah Hockey Club


def run_analysis_pipeline():
    print("Running analysis pipeline...")

    df = pd.read_csv("nhl_players_cleaned.csv")

    gaps = compute_team_gaps(df, TEAM_ABBREV)

    # print(gaps)

    fig = plot_team_gaps(gaps)
    fig.savefig("mammoth_gaps.png", dpi=300, bbox_inches="tight")

    for pos in ["R", "C", "L", "D"]:
      gaps = compute_team_gaps_pos(df, "UTA", pos)

    posfig = plot_position_gaps(gaps, pos)
    posfig.savefig(f"mammoth_gaps{pos}.png", dpi = 300)

    fig = scatter_metric_by_position(df, "UTA", "F", "TOI/GP", "P/GP")
    fig.savefig("scatter_F_TOI_PGP.png", dpi=300)


    # Defense
    gaps_D = compute_team_gaps_pos(df, "UTA", "D")
    # gaps_D.to_csv("mammoth_defense_gaps.csv")
    # print(gaps_D)
    fig = plot_position_gaps(gaps_D, "D")
    fig.savefig("gaps_D.png", dpi = 300)

    #Forwards
    forward_gaps = compute_all_forward_gaps(df, "UTA")
    # forward_gaps.to_csv("mammoth_gaps_all_forwards.csv", index=False)

    fig = plot_all_forward_gaps(forward_gaps)
    fig.savefig("mammoth_gaps_all_forwards.png", dpi=300)


    # Forwards (separated)
    for pos in ["C", "L", "R"]:

      gaps = compute_forward_position_gaps(df, "UTA", pos)

      # gaps.to_csv(f"mammoth_gaps_{pos}.csv", index=False)

      fig = plot_forward_position_gaps(gaps, pos)
      fig.savefig(f"mammoth_gaps_{pos}.png", dpi=300)


    print("All analyses complete!")
    print("Outputs written to current directory.")


def compute_team_gaps(df, team_abbrev):
    metrics = ["G", "A", "P", "S", "PIM", "+/-"]

    team = df[df["Team"] == team_abbrev]
    league = df

    df_out = pd.DataFrame({
        "team_median": team[metrics].median(),
        "league_median": league[metrics].median(),
    })

    df_out["gap"] = df_out["league_median"] - df_out["team_median"]
    return df_out


def plot_team_gaps(gaps):
    fig, ax = plt.subplots(figsize=(8, 5))

    ax.bar(gaps.index, gaps["gap"])
    ax.set_title("Utah Mammoth vs League Median")
    ax.set_ylabel("League median - Mammoth median")
    ax.tick_params(axis="x", rotation=45)

    fig.tight_layout()
    return fig

def compute_team_gaps_pos(df, team_abbrev, position):
    metrics = ["G", "A", "P", "S", "PIM", "+/-"]

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
            "gap":league[metric].median() - team[metric].median()
          })

    return pd.DataFrame(results)


def plot_position_gaps(gaps, position):
    fig, ax = plt.subplots(figsize=(10, 5))

    labels = [f"{pos}-{metric}" for pos, metric in zip(gaps["position"], gaps.index)]

    ax.bar(labels, gaps["gap"])
    ax.axhline(0, linestyle="--")

    ax.set_title(f"Utah Mammoth vs League Median ({position})")
    ax.set_ylabel("League median − Mammoth median")
    ax.tick_params(axis="x", rotation=45)

    fig.tight_layout()
    return fig

def plot_forward_metric_groups(gaps):
    fig, ax = plt.subplots(figsize=(10, 5))

    metrics = gaps["metric"].unique()
    positions = ["C", "L", "R"]
    width = 0.25

    for i, pos in enumerate(positions):
        pos_data = gaps[gaps["position"] == pos]
        ax.bar(
            range(len(metrics)),
            pos_data["gap"],
            width=width,
            label=pos,
            offset=width * i
        )

    ax.set_xticks([r + width for r in range(len(metrics))])
    ax.set_xticklabels(metrics)
    ax.axhline(0, linestyle="--")

    ax.set_title("Utah Mammoth vs League Median — Forwards")
    ax.set_ylabel("League median − Mammoth median")
    ax.legend()

    fig.tight_layout()
    return fig



def scatter_metric_by_position(df, team_abbrev, position, x, y):
    df_pos = df[df["Pos"] == position]

    fig, ax = plt.subplots(figsize=(7, 6))

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
    metrics = ["G", "A", "P", "S", "PIM", "+/-"]

    df_forwards = df[df["Pos"].isin(["C", "L", "R"])]

    team = df_forwards[df_forwards["Team"] == team_abbrev]
    league = df_forwards

    gaps = {
        metric: league[metric].median() - team[metric].median()
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
    metrics = ["G", "A", "P", "S", "PIM", "+/-"]

    df_pos = df[df["Pos"] == position]

    team = df_pos[df_pos["Team"] == team_abbrev]
    league = df_pos

    gaps = {
        metric: league[metric].median() - team[metric].median()
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
