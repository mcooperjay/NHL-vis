import pandas as pd
import matplotlib.pyplot as plt


TEAM = "UTA"   # Utah Mammoth / Utah Hockey Club


def run_analysis_pipeline():
    print("Running analysis pipeline...")
    #Loading the data and Constants
    df = pd.read_csv("src/nhl_vis_386/nhl_players_cleaned.csv")
    COUNT_METRICS = ["G", "A", "P", "S", "PIM", "+/-"]
    PERCENT_METRICS = ["S%", "FOW%"]
    df_count = dropna_metric(df, COUNT_METRICS)
    df_perc = dropna_metric(df, PERCENT_METRICS)
    #Team v League
    gaps_counts = compute_team_gaps(df_count, TEAM, COUNT_METRICS)
    fig = plot_team_gaps(gaps_counts)
    fig.savefig("docs/count_mammoth_gaps.png", dpi=300, bbox_inches="tight")
    
    gaps_perc = compute_team_gaps(df_perc, TEAM, PERCENT_METRICS)
    fig = plot_team_gaps(gaps_perc)
    fig.savefig("docs/perc_mammoth_gaps.png", dpi=300, bbox_inches="tight")
    #Forwards
    forward_gaps_counts = compute_forward_gaps(df_count, TEAM, COUNT_METRICS)
    fig = plot_all_forward_gaps(forward_gaps_counts)
    fig.savefig("docs/forwards_gaps_counts.png", dpi=300)

    forward_gaps_perc = compute_forward_gaps(df_perc, TEAM, PERCENT_METRICS)
    fig = plot_all_forward_gaps(forward_gaps_perc)
    fig.savefig("docs/forwards_gaps_percentages.png", dpi=300)

    #Forwards and Defense separated out
    for pos in ["C", "L", "R", "D"]:

        # ---- Count metrics
        df_pos_counts = dropna_metric(df, COUNT_METRICS)
        gaps_counts = compute_position_gaps(
            df_pos_counts, TEAM, pos, COUNT_METRICS
        )
        fig = plot_forward_position_gaps(gaps_counts, pos)
        fig.savefig(f"docs/{pos}_counts.png", dpi=300)

        # ---- Percentage metrics
        df_pos_perc = dropna_metric(df, PERCENT_METRICS)
        gaps_perc = compute_position_gaps(
            df_pos_perc, TEAM, pos, PERCENT_METRICS
        )
        fig = plot_forward_position_gaps(gaps_perc, pos)
        fig.savefig(f"docs/{pos}_percentages.png", dpi=300)
    df_scatter = df.dropna(subset=["TOI/GP", "P/GP"])
    fig = scatter_metric_by_position(df_scatter, TEAM, "F", "TOI/GP", "P/GP")
    fig.savefig("docs/scatter_F_TOI_PGP.png", dpi=300)

    print("All analyses complete!")

def compute_team_gaps(df, team_abbrev, metrics):

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
    ax.set_ylabel("Utah − League (median)")
    ax.tick_params(axis="x", rotation=45)
    ax.axhline(0, linestyle="--")

    fig.tight_layout()
    return fig

def plot_position_gaps(gaps, position):
    fig, ax = plt.subplots(figsize=(8, 5))

    labels = [f"{pos}-{metric}" for pos, metric in zip(gaps["position"], gaps.index)]

    ax.bar(labels, gaps["gap"])
    ax.axhline(0, linestyle="--")

    ax.set_title(f"Utah Mammoth vs League Median ({position})")
    ax.set_ylabel("Utah − League (median)")
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

def compute_forward_gaps(df, team_abbrev, metrics):

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
    ax.set_ylabel("Utah − League (median)")
    ax.tick_params(axis="x", rotation=45)

    fig.tight_layout()
    return fig

def compute_position_gaps(df, team_abbrev, position, metrics):

    df_pos = df[df["Pos"] == position]

    team = df_pos[df_pos["Team"] == team_abbrev]
    league = df_pos

    gaps = {
        metric: team[metric].median() - league[metric].median()
        for metric in metrics
        if metric in df_pos.columns
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
    ax.set_ylabel("Utah − League (median)")
    ax.tick_params(axis="x", rotation=45)

    fig.tight_layout()
    return fig

def dropna_metric(df, metrics):
  return df.dropna(subset=metrics)

if __name__ == "__main__":
    run_analysis_pipeline()