---
 title: nhl_vis_386
 author: Timothy Hardy and Cooper Maughan
---

Class package to analyze NHL player data from the last 25 years.

## Description

This package features:
- Data acquisition functions
- Data aggregation/filtering functions to get stats from specific players and seasons
- Data filters to get stats from a specific team/season roster
- Functions to visualize NHL player stats relative to the rest of the league

## Installation

```bash
pip install nhl-vis-386 
```

## Usage

```python
# Get stats for a player in specific seasons, unaggregated
get_player_stats("Connor Bedard", season=[2023, 2024], aggr=False)

# Get stats for a team's roster
get_roster_stats("CHI", 2024)

# Visualize scatterplot of common metrics, highlighting a team and player
score_scatter(player="Connor Bedard", season = 2024, metrics = ["A", "G"])

# Visualize a player's scoring relative to the league average
score_plot("Connor Bedard", season=2024)
```

The full documentation can be found (here)[https://github.com/mcooperjay/NHL-vis/documentation.md]

## License

MIT