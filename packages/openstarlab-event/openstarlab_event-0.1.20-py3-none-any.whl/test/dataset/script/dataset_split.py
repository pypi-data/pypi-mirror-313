import pandas as pd
import os
import pdb

def split_dataset(id_matching_csv:str,event_data_csv:str):
    #read id_list
    id_list = pd.read_csv(id_matching_csv)

    #order the id_list by the match_date_statsbomb
    id_list = id_list.sort_values("match_date_statsbomb").reset_index(drop=True)

    #split the id_list into train, validation and test with 60%, 20%, 20% respectively
    train_size = int(0.6 * len(id_list)) #228
    val_size = int(0.2 * len(id_list)) #76
    test_size = len(id_list) - train_size - val_size #76
    print(f"train_size: {train_size}, val_size: {val_size}, test_size: {test_size}")

    train_id_list = id_list.iloc[:train_size].match_id_statsbomb.to_list()
    val_id_list = id_list.iloc[train_size:train_size+val_size].match_id_statsbomb.to_list()
    test_id_list = id_list.iloc[train_size+val_size:].match_id_statsbomb.to_list()

    #load the preprocessed event data
    event_data = pd.read_csv(event_data_csv)

    #split the event_data into train, validation and test
    train_event_data = event_data[event_data.match_id.isin(train_id_list)]
    val_event_data = event_data[event_data.match_id.isin(val_id_list)]
    test_event_data = event_data[event_data.match_id.isin(test_id_list)]

    return train_event_data, val_event_data, test_event_data

if __name__ == "__main__":
    id_matching_csv = "/home/c_yeung/workspace6/python/openstarlab/Event/test/dataset/csv/id_matching.csv"
    event_data_csv = "/home/c_yeung/workspace6/python/openstarlab/Event/test/dataset/csv/data.csv"
    save_dir = "/home/c_yeung/workspace6/python/openstarlab/Event/test/dataset/csv"
    train_event_data, val_event_data, test_event_data = split_dataset(id_matching_csv, event_data_csv)
    train_event_data.to_csv(os.path.join(save_dir, "train.csv"), index=False)
    val_event_data.to_csv(os.path.join(save_dir, "valid.csv"), index=False)
    test_event_data.to_csv(os.path.join(save_dir, "test.csv"), index=False)
