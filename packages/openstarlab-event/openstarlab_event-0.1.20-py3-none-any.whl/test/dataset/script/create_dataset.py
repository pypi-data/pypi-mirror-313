import os
import json
from tqdm import tqdm
import pandas as pd
from statsbombpy import sb

from preprocessing import Event_data

#down_load_statsbomb_data function
def download_statsbomb_data(creds, save_dir,competition_id=11, season_id=281):

    os.makedirs(save_dir, exist_ok=True)

    def convert_df_in_dict(d):
        for key, value in d.items():
            if isinstance(value, pd.DataFrame):
                d[key] = value.to_dict(orient='records')
            elif isinstance(value, dict):
                convert_df_in_dict(value)
        return d

    # Get Statsbomb matches data
    matches = sb.matches(competition_id=competition_id, season_id=season_id, creds=creds)
    matches["competition_id"] = competition_id
    matches["season_id"] = season_id
    #moev the competition_id and season_id to the first column
    cols = matches.columns.tolist()
    cols = cols[-2:] + cols[:-2]
    matches = matches[cols]
    #save the matches to csv
    matches.to_csv(os.path.join(save_dir, "matches.csv"), index=False)

    # Get Statsbomb lineups and events
    os.makedirs(os.path.join(save_dir, "lineups"), exist_ok=True)
    os.makedirs(os.path.join(save_dir, "events"), exist_ok=True)
    for match_id in tqdm(matches["match_id"].unique()):
        lineups = sb.lineups(match_id=match_id, creds=creds)
        events = sb.events(match_id=match_id, include_360_metrics=True, creds=creds)
        events.to_csv(os.path.join(save_dir, "events", f"{match_id}.csv"), index=False)
        #save the lineups as json and with row changes
        lineups = convert_df_in_dict(lineups)
        with open(os.path.join(save_dir, "lineups", f"{match_id}.json"), "w") as f:
            json.dump(lineups, f, indent=4)

if __name__ == "__main__":
    #Statsbomb API
    # creds = {"user": "input your Statsbomb api user name here", "passwd": "input your Statsbomb api password here"}
    #Statsbomb event data saving dir
    # save_dir = "/home/c_yeung/workspace6/python/openstarlab/EventModeling/test/dataset/"
    #path to the skillcorner tracking data
    tracking_path="/skillcorner/tracking"
    #path to the skillcorner match data
    match_path="/skillcorner/match"

    statsbomb_skillcorner_event_path="/data_pool_1/laliga_23/statsbomb/events"
    statsbomb_skillcorner_tracking_path="/data_pool_1/laliga_23/skillcorner/tracking"
    statsbomb_skillcorner_match_path="/data_pool_1/laliga_23/skillcorner/match"

    # download_statsbomb_data(creds, save_dir)

    #output file
    match_id_df_path="/home/c_yeung/workspace6/python/openstarlab/Event/test/dataset/csv/id_matching.csv"
    output_dir="/home/c_yeung/workspace6/python/openstarlab/Event/test/dataset/csv/data.csv"
    # match_id_df_path="/home/c_yeung/workspace6/python/openstarlab/Event/test/dataset/csv/id_matching_test.csv"
    # output_dir="/home/c_yeung/workspace6/python/openstarlab/Event/test/dataset/script/bug_test/data_test.csv"

    #Match the statsbomb and skillcorner (multiple files)
    statsbomb_skillcorner_df=Event_data(data_provider='statsbomb_skillcorner',
                                        statsbomb_event_dir=statsbomb_skillcorner_event_path,
                                        skillcorner_tracking_dir=statsbomb_skillcorner_tracking_path,
                                        skillcorner_match_dir=statsbomb_skillcorner_match_path,
                                        match_id_df=match_id_df_path, 
                                        preprocess_method="UIED"
                                        ).preprocessing()
    statsbomb_skillcorner_df.to_csv(output_dir,index=False)
    print("---------------done-----------------")

    