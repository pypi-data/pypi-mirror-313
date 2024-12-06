import pandas as pd
import pdb

df_path= "/home/c_yeung/workspace6/python/openstarlab/Event/test/dataset/csv/train.csv"
df = pd.read_csv(df_path)

# found the len of the possession with "poss_id"
possession_len = df.groupby(['match_id', 'poss_id']).size().reset_index(name='len')
#get the stats of the possession length
possession_len_stats = possession_len['len'].describe()
#get the 99% percentile of the possession length
possession_len_99 = possession_len['len'].quantile(0.99)
pdb.set_trace() 
"""
for train.csv, possession_len_stats is:
count    56481.000000
mean         7.650484
std          8.746516
min          2.000000
25%          2.000000
50%          4.000000
75%          9.000000
max        127.000000
"""