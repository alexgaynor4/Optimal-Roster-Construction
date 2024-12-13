import pandas as pd

# Load datasets
salaries_1997_2019 = pd.read_csv('Salaries 1996-2021.csv')
totals_stats = pd.read_csv('totals_stats.csv')
all_seasons = pd.read_csv('all_seasons.csv')
salary_cap = pd.read_csv('salary_caps.csv')

# Filter salaries_1997_2019 for seasons from 2017 onwards
salaries_1997_2019 = salaries_1997_2019[salaries_1997_2019['seasonStartYear'] >= 2017]

# Filter all_seasons for seasons from 2017 onwards
all_seasons = all_seasons[all_seasons['season'].str[:4].astype(int) >= 2017]
totals_stats['Season'] = totals_stats['Season'].str[:4].astype(int)
totals_stats = totals_stats[totals_stats['Season'] >= 2017]

# Standardize player names in totals_stats and all_seasons
salaries_1997_2019['playerName'] = salaries_1997_2019['playerName'].str.lower().str.strip().str.replace(r'[^a-zA-Z0-9 ]', '', regex=True)
totals_stats['Player'] = totals_stats['Player'].str.lower().str.strip().str.replace(r'[^a-zA-Z0-9 ]', '', regex=True)
all_seasons['player_name'] = all_seasons['player_name'].str.lower().str.strip().str.replace(r'[^a-zA-Z0-9 ]', '', regex=True)

salary_cap = salary_cap[salary_cap['Year'].str[:4].astype(int) >= 2017]
salary_cap['Salary Cap'] = salary_cap['Salary Cap'].replace('[\$,]', '', regex=True).astype(float)
salary_cap['seasonStartYear'] = salary_cap['Year'].str[:4].astype(int)

# Merge salaries_1997_2019 with totals_stats
merged_data_1997_2019 = pd.merge(
    salaries_1997_2019,
    totals_stats[['Player', 'Tm', 'Age', 'Season']],
    left_on=['playerName', 'seasonStartYear'],
    right_on=['Player', 'Season'],
    how='left'
).drop(columns=['Player', 'Season', 'inflationAdjSalary'])

merged_data_1997_2019.columns = ['Player', 'Season', 'Salary', 'Team', 'Age']
all_seasons['season'] = all_seasons['season'].str[:4].astype(int)
all_seasons = all_seasons[all_seasons['season'] >= 2017]
print(all_seasons)

# Merge the combined dataset with all_seasons
final_merged_data = pd.merge(
    merged_data_1997_2019,
    all_seasons[['player_name', 'team_abbreviation', 'age', 'season', 'usg_pct']],
    left_on=['Player', 'Season'],
    right_on=['player_name', 'season'],
    how='left'
)
# Drop redundant columns
final_merged_data = final_merged_data.drop(columns=['player_name', 'team_abbreviation', 'season', 'age'])
print(final_merged_data)

final_dataset = pd.merge(
    final_merged_data,
    salary_cap[['seasonStartYear', 'Salary Cap']],
    left_on='Season',
    right_on='seasonStartYear',
    how='left'
).drop('seasonStartYear', axis=1)

final_dataset = final_dataset.drop_duplicates()
# Convert salary column to float
final_dataset['Salary'] = final_dataset['Salary'].replace('[\$,]', '', regex=True).astype(float)

# Calculate the percent of salary cap for each player
final_dataset['PercentSalaryCap'] = (final_dataset['Salary'] / final_dataset['Salary Cap']) * 100

final_dataset = final_dataset[final_dataset['Team'] != 'TOT']
final_dataset = final_dataset.rename(columns={'usg_pct':'UsageRate'})
final_dataset = final_dataset.dropna()
final_dataset = final_dataset.groupby(['Team', 'Season']).apply(lambda x: x.nlargest(12, 'Salary')).reset_index(drop=True)
# Save the final dataset to a CSV file
final_dataset.to_csv('final_player_dataset_2017_2023.csv', index=False)

# Display the final dataset
print(final_dataset.head())

final_dataset.groupby(['Team', 'Season'])['PercentSalaryCap'].agg('sum').to_csv("Total Salaries.csv")