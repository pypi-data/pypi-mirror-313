import pandas as pd
import numpy as np
import pdb

train_path= "/home/c_yeung/workspace6/python/openstarlab/Event/test/dataset/csv/train.csv"
train_df = pd.read_csv(train_path)

#count action=shot and success
# shot_df = train_df[(train_df["action"]=="shot") & (train_df["goal"]==1)]
# print("Number of successful shots: ", shot_df.shape[0])
# shot_df = train_df[(train_df["action"]=="shot") & (train_df["goal"]==0)]
# print("Number of failed shots: ", shot_df.shape[0])
'''
Number of successful shots:  581
Number of failed shots:  4995
'''

# train_df.action.value_counts()
'''
short_pass     168607
carry          147316
_               56481
high_pass       38831
cross            7841
dribble          6488
shot             5576
long_pass         517
period_over       225
game_over         225
'''


poss_len_data=[]
for i in train_df.match_id.unique():
    match_df = train_df[train_df["match_id"]==i]
    for j in match_df.poss_id.unique():
        poss_df = match_df[match_df["poss_id"]==j]
        poss_len_data.append(poss_df.shape[0])

#print the mean and standard deviation of the number of events in each possession
print("Mean number of events in each possession: ", np.mean(poss_len_data))
print("Standard deviation of the number of events in each possession: ", np.std(poss_len_data))
#print the maximum and minimum number of events in each possession
print("Maximum number of events in each possession: ", max(poss_len_data))
print("Minimum number of events in each possession: ", min(poss_len_data))
'''
Mean number of events in each possession:  7.65048423363609
Standard deviation of the number of events in each possession:  8.74643868143599
Maximum number of events in each possession:  127
Minimum number of events in each possession:  2

97.9% of possessions have 25.1434 events or less
99.9% of possessions have 33.8898 events or less
'''
pdb.set_trace()