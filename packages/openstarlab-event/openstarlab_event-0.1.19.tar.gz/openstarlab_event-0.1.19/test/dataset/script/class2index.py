import pandas as pd

data_path='/home/c_yeung/workspace6/python/openstarlab/Event/test/dataset/csv/data.csv'

df = pd.read_csv(data_path)

#get the unique values of the action and team columns
unique_actions = df["action"].unique()
unique_teams = df["team"].unique()

#map the unique values to integers in a dictionary and print the dictionary
action2index = {action: index for index, action in enumerate(unique_actions)}
team2index = {team: index for index, team in enumerate(unique_teams)}
print("Action to index mapping: ", action2index)
print("Team to index mapping: ", team2index)

'''
Action to index mapping:  {'short_pass': 0, 'carry': 1, 'high_pass': 2, '_': 3, 'cross': 4, 'long_pass': 5, 'shot': 6, 'dribble': 7, 'period_over': 8, 'game_over': 9}
Team to index mapping:  {'Granada': 0, 'Atlético Madrid': 1, 'Celta Vigo': 2, 'Osasuna': 3, 'Valencia': 4, 'Sevilla': 5, 'Mallorca': 6, 'Las Palmas': 7, 'Cádiz': 8, 'Deportivo Alavés': 9, 'Real Sociedad': 10, 'Girona': 11, 'Villarreal': 12, 'Real Betis': 13, 'Barcelona': 14, 'Getafe': 15, 'Rayo Vallecano': 16, 'Almería': 17, 'Athletic Club': 18, 'Real Madrid': 19}
'''