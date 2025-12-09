# NHL-Vis-386

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
- Team abbreviation (based on official NHL abbreviations)
# add link above
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



## Data Analysis