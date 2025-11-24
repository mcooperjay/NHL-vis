import requests
import pandas as pd

def get_nhl_skater_page(season_id, page_num, page_size=100):
    base_url = "https://api.nhle.com/stats/rest/en/skater/summary"
    
    params = {
        "isAggregate": "false",
        "reportType": "season",
        "isGame": "false",
        "reportName": "skatersummary",
        "sort": '[{"property":"points","direction":"DESC"}]',
        "cayenneExp": f"gameTypeId=2 and seasonId={season_id}",
        "start": page_num * page_size,
        "limit": page_size
    }
    
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    data = response.json()
    
    return pd.DataFrame(data.get("data", []))

# Loop through seasons
all_pages = []
page_size = 100
seasons =  [20002001, 20012002, 20022003, 20032004, 20042005,
            20052006, 20062007, 20072008, 20082009, 20092010,
            20102011, 20112012, 20122013, 20132014, 20142015,
            20152016, 20162017, 20172018, 20182019, 20192020,
            20202021, 20212022, 20222023, 20232024, 20242025]

for season in seasons:
    page_num = 0
    while True:
        df = get_nhl_skater_page(season, page_num, page_size)
        if df.empty:
            break
        all_pages.append(df)
        page_num += 1
        print(f"Season {season}, page {page_num}, rows: {len(df)}")

# Combine and clean
all_data = pd.concat(all_pages, ignore_index=True)

all_data.to_csv("nhl_skater_stats_2000_2024.csv", index=False)

print(f"Total rows: {len(all_data)}")
