---
title: NHL-Vis-386 Documentation
author: Timothy Hardy and Cooper Maughan
---

## Package Installation and Import

Install NHL-Vis-386 with the following code:

```bash
pip install nhl-vis-386
```

Then, use it in your python script with the following (or your desired import):

```python
import nhl_vis_386 as nhl
```

## Primary Dataset

Data in this package has been gathered from the [official NHL website](https://www.nhl.com/stats/skaters). Below is a description of each variable. Data has been pulled from the 2000-2024 NHL seasons, and is accessed in the `nhl.df` object.

| Variable  | Description |
|-----------|-------------|
| Player  | First and Last name of a player |
| Team | Three letter team abbreviation as given by [NHL.com](NHL.com)|
| A | Assists |
| EVG | Even-strength Goals |
| EVP | Even-strength Points |
| FOW% | Faceoff Win Percentage |
| GWG | Game-winning Goals |
| GP | Games Played |
| G | Goals scored |
| OTG | Overtime Goals |
| PIM | Penalty Minutes (minutes) |
| playerID | Unique player identifier |
| +/- | Plus-minus; Gives a team's point differential while a player is on the ice |
| P | Points |
| P/GP | Points per Game |
| Pos | Position (C, R, L, W) |
| PPG | Powerplay Goals |
| PPP | Powerplay Points |
| Season | 4 digits representing the year that a season started |
| SHG | Short-handed goals |
| SHP | Short-handed points |
| S% | Shooting percentage |
| S/C | Which hand the player shoots/catches with | 
| S | Shots taken |
| TOI/GP | Time on ice per game played (seconds) |



## Data Acquisition


### Get stats for a player

The function `get_player_stats` takes in the following:
- Player name
- Season(s). Optional argument, can be passed in as an integer or a list.
- Aggr- Aggregates all available seasons into a single row if True. If False, returns individual season rows.

It then returns a pd.DataFrame with the requested statistics.

Example usage:

```python
get_player_stats("Connor Bedard", season=[2023, 2024], aggr=False)
```

### Get stats for a roster

The function `get_roster_stats` takes in the following:
- Team abbreviation (based on (official NHL abbreviations)[https://en.wikipedia.org/wiki/Wikipedia:WikiProject_Ice_Hockey/NHL_team_abbreviations])
- Season- integer

It then returns a pd.DataFrame with the requested roster statistics.

Example usage:

```python
get_roster_stats("CHI", 2024)
```


Visualize scatterplot of common metrics, highlighting a team and player
score_scatter(player="Connor Bedard", season = 2024, metrics = ["A", "G"])

Visualize a player's scoring relative to the league average
score_plot("Connor Bedard", season=2024)



## Data Visualization


There are two main functions in this package for data visualization.

### Plot player data relative to league average

The function `score_plot` takes in the following:

- Player name
- Season (default- 2024)
- Metrics (official metrics in a list, default shows points, goals, and assists)
- df- Optional pd.DataFrame object

It then returns a Plotly figure showing that player's metrics relative to the rest of the league.

Example usage:

```python
custom_df = df.copy() # Any desired filters (e.g. by position)
score_plot("Connor Bedard", season=2023, metrics=["S%", "PIM", "P"], df=custom_df)
```

### Plot league-wide scatterplots

The function `score_scatter` takes in the following:

Player- A specific player to highlight, None by default
Season- None by default
Team- A specific team to highlight, None by default
Metrics- A list of two metrics to display. Shows Goals and Assists by default.
df- Optional pd.DataFrame object.

It then returns a scatterplot with desired highlights and metrics. Discrete or continuous variables may be used.

Example usage:

```python
score_scatter(player="Connor Bedard", season=2024, team = "UTA", metrics=["S%", "Pos"])
```