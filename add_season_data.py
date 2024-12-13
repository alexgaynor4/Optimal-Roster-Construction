import pandas as pd

# Load the datasets
team_stats = pd.read_csv('team_stats.csv')
team_stats_playoffs = pd.read_csv('team_stats_playoffs.csv')
team_salary_statistics = pd.read_csv('team_salary_statistics_new.csv')

# Filter team_stats to include data from the 2000 season onwards
team_stats['season'] = team_stats['season'].str[:4].astype(int)
team_stats = team_stats[team_stats['season'] >= 2000]

# Filter team_stats_playoffs to include data from the 2000 season onwards
team_stats_playoffs['season'] = team_stats_playoffs['season'].str[:4].astype(int)
team_stats_playoffs = team_stats_playoffs[team_stats_playoffs['season'] >= 2017]

# Filter team_salary_statistics to include data from the 2000 season onwards
team_salary_statistics['season'] = team_salary_statistics['season'].astype(int)
team_salary_statistics = team_salary_statistics[team_salary_statistics['season'] >= 2017]
team_salary_statistics = team_salary_statistics[team_salary_statistics['team'] != "TOT"]

# Mapping of team abbreviations to full names
team_name_mapping = {
    'ATL': 'Atlanta Hawks', 'BOS': 'Boston Celtics', 'BRK': 'Brooklyn Nets', 'CHA': 'Charlotte Hornets',
    'CHI': 'Chicago Bulls', 'CLE': 'Cleveland Cavaliers', 'DAL': 'Dallas Mavericks', 'DEN': 'Denver Nuggets',
    'DET': 'Detroit Pistons', 'GSW': 'Golden State Warriors', 'HOU': 'Houston Rockets', 'IND': 'Indiana Pacers',
    'LAC': 'Los Angeles Clippers', 'LAL': 'Los Angeles Lakers', 'MEM': 'Memphis Grizzlies', 'MIA': 'Miami Heat',
    'MIL': 'Milwaukee Bucks', 'MIN': 'Minnesota Timberwolves', 'NOP': 'New Orleans Pelicans', 'NYK': 'New York Knicks',
    'OKC': 'Oklahoma City Thunder', 'ORL': 'Orlando Magic', 'PHI': 'Philadelphia 76ers', 'PHO': 'Phoenix Suns',
    'POR': 'Portland Trail Blazers', 'SAC': 'Sacramento Kings', 'SAS': 'San Antonio Spurs', 'TOR': 'Toronto Raptors',
    'UTA': 'Utah Jazz', 'WAS': 'Washington Wizards', 'CHH': 'Charlotte Hornets', 'NJN': 'New Jersey Nets', 'SEA': 'Seattle Supersonics',
    'VAN': 'Vancouver Grizzlies', 'NOH': 'New Orleans Hornets', 'NOK': 'New Orleans Hornets', 'CHO': 'Charlotte Hornets'
}
team_salary_statistics['team'] = team_salary_statistics['team'].map(team_name_mapping)

# Merge the team_stats with the team_salary_statistics on season and team
merged_stats = pd.merge(
    team_salary_statistics, 
    team_stats[['season', 'Team', 'win_percentage']], 
    left_on=['season', 'team'], 
    right_on=['season', 'Team'], 
    how='left'
)

# Drop redundant 'Team' column
merged_stats = merged_stats.drop(columns=['Team'])

# Merge the team_stats_playoffs with the merged_stats on season and team
final_merged_stats = pd.merge(
    merged_stats, 
    team_stats_playoffs[['season', 'team', 'wins']], 
    left_on=['season', 'team'], 
    right_on=['season', 'team'], 
    how='left'
)

# Rename columns for clarity
final_merged_stats.rename(columns={'win_percentage': 'regular_season_win_percentage', 'wins': 'playoff_wins'}, inplace=True)
final_merged_stats['playoff_wins'] = final_merged_stats['playoff_wins'].fillna(0)
# Save the final merged dataset to a CSV file
final_merged_stats.to_csv('final_team_salary_statistics_new.csv', index=False)

# Display the first few rows of the final dataset
print(final_merged_stats.head())
