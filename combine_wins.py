import pandas as pd

data_regular = pd.read_csv('Team Clusters Regular.csv')
data_playoffs = pd.read_csv('Team Clusters Playoffs.csv')
data_regular = data_regular.sort_values(axis=0, by="High Usage, Mid Age, High Salary")
data_regular = data_regular.drop(['Unnamed: 0.1','Unnamed: 0'], axis=1)
data_regular.to_csv('Team Clusters Regular.csv', index=False)