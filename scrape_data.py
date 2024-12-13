import requests
from bs4 import BeautifulSoup
import pandas as pd
from unidecode import unidecode
import re
import time

years = [2018, 2019, 2020, 2021, 2022, 2023, 2024]
teams = []
wins = []
years_list = []
teams_list = {
    'Atlanta Hawks': 'ATL','Boston Celtics': 'BOS','Brooklyn Nets': 'BRK','Charlotte Hornets': 'CHO','Chicago Bulls': 'CHI',
    'Cleveland Cavaliers': 'CLE','Dallas Mavericks': 'DAL','Denver Nuggets': 'DEN','Detroit Pistons': 'DET','Golden State Warriors': 'GSW',
    'Houston Rockets': 'HOU','Indiana Pacers': 'IND','Los Angeles Clippers': 'LAC','Los Angeles Lakers': 'LAL','Memphis Grizzlies': 'MEM',
    'Miami Heat': 'MIA','Milwaukee Bucks': 'MIL','Minnesota Timberwolves': 'MIN','New Orleans Pelicans': 'NOP','New York Knicks': 'NYK',
    'Oklahoma City Thunder': 'OKC','Orlando Magic': 'ORL','Philadelphia 76ers': 'PHI','Phoenix Suns': 'PHO','Portland Trail Blazers': 'POR',
    'Sacramento Kings': 'SAC','San Antonio Spurs': 'SAS','Toronto Raptors': 'TOR','Utah Jazz': 'UTA','Washington Wizards': 'WAS'
}
for year in years:
# Define the URL to scrape data from
    url = f'https://www.basketball-reference.com/playoffs/NBA_{year}.html'
    teams_this_year = []
    time.sleep(20)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find all rows in the table

    rows = soup.select('#advanced-team tbody tr')
    tables = soup.find_all('table')
    for row in rows:
        print(2)
        # Extract team name
        team_tag = row.find('a')
        if team_tag:
            team_name = team_tag.text.strip()
            teams.append(team_name)
            teams_this_year.append(team_name)
            wins_tag = row.find('td', {'data-stat': 'wins'})
            if wins_tag:
                win_count = wins_tag.text.strip()
                wins.append(win_count)
            years_list.append(int(year) - 1)

# Create a DataFrame
team_wins_df = pd.DataFrame({
    'Team': teams,
    'Wins': wins,
    'Season': years_list
})

# Save to CSV
team_wins_df.to_csv('team_wins.csv', index=False)

# Print the DataFrame
print(team_wins_df)
