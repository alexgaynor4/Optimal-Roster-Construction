import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

# Load the final dataset with clusters
cluster_counts_all_seasons = pd.read_csv('Team Cluster Counts.csv')
team_stats = pd.read_csv('team_stats.csv')
team_stats_playoffs = pd.read_csv('team_wins.csv')

team_name_to_abbr = {
    'Atlanta Hawks': 'ATL','Boston Celtics': 'BOS','Brooklyn Nets': 'BRK','Charlotte Hornets': 'CHO','Chicago Bulls': 'CHI',
    'Cleveland Cavaliers': 'CLE','Dallas Mavericks': 'DAL','Denver Nuggets': 'DEN','Detroit Pistons': 'DET','Golden State Warriors': 'GSW',
    'Houston Rockets': 'HOU','Indiana Pacers': 'IND','Los Angeles Clippers': 'LAC','LA Clippers': 'LAC','Los Angeles Lakers': 'LAL','Memphis Grizzlies': 'MEM',
    'Miami Heat': 'MIA','Milwaukee Bucks': 'MIL','Minnesota Timberwolves': 'MIN','New Orleans Pelicans': 'NOP','New York Knicks': 'NYK',
    'Oklahoma City Thunder': 'OKC','Orlando Magic': 'ORL','Philadelphia 76ers': 'PHI','Phoenix Suns': 'PHO','Portland Trail Blazers': 'POR',
    'Sacramento Kings': 'SAC','San Antonio Spurs': 'SAS','Toronto Raptors': 'TOR','Utah Jazz': 'UTA','Washington Wizards': 'WAS'
}

# Map full team names to abbreviations
team_stats['Team'] = team_stats['Team'].map(team_name_to_abbr)
team_stats_playoffs['Team'] = team_stats_playoffs['Team'].map(team_name_to_abbr)

# Shorten the season format to just the starting year
team_stats['season'] = team_stats['season'].str[:4].astype(int)
#team_stats_playoffs['Season'] = team_stats_playoffs['Season'].str[:4].astype(int)

# Merge the cluster counts with the regular season team stats using win percentage
merged_data_regular = pd.merge(cluster_counts_all_seasons, team_stats[['Team', 'season', 'win_percentage']], left_on=['Season', 'Team'], right_on=['season', 'Team'], how='inner')

# Merge the cluster counts with the playoff team stats using number of wins
merged_data_playoff = pd.merge(cluster_counts_all_seasons, team_stats_playoffs[['Team', 'Season', 'Wins']], left_on=['Season', 'Team'], right_on=['Season', 'Team'], how='inner')

# Drop redundant columns
merged_data_regular = merged_data_regular.drop(columns=['season'])
#merged_data_playoff = merged_data_playoff.drop(columns=['season', 'team'])

merged_data_regular.to_csv("Team Clusters Regular.csv", index=False)
merged_data_playoff.to_csv("Team Clusters Playoffs.csv", index=False)

