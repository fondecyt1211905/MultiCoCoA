import database.directdb as directdb
import pandas as pd

def get_df(indicator_name, id_analysis):
    db = directdb.connect()
    indicator = db[indicator_name]
    results = indicator.find({"id_analysis": id_analysis})
    documents=list(results)
    df = pd.DataFrame(documents)
    df_measures = df["measures"]
    df = df.drop(columns=['measures'])
    df_measures = pd.DataFrame(df_measures.to_list())
    df = pd.concat([df, df_measures], axis=1)
    df = df.drop(columns=['_id'])
    return df

def concat_df_apm(df1, df2):
    df = pd.concat([df1, df2[['F0final_sma_maxPos',
        'F0final_sma_minPos', 'F0final_sma_amean', 'F0final_sma_stddev',
        'pcm_loudness_sma_maxPos', 'pcm_loudness_sma_minPos',
        'pcm_loudness_sma_amean', 'pcm_loudness_sma_stddev',
        'jitterLocal_sma_maxPos', 'jitterLocal_sma_minPos',
        'jitterLocal_sma_amean', 'jitterLocal_sma_stddev',
        'jitterDDP_sma_maxPos', 'jitterDDP_sma_minPos', 'jitterDDP_sma_amean',
        'jitterDDP_sma_stddev', 'shimmerLocal_sma_maxPos',
        'shimmerLocal_sma_minPos', 'shimmerLocal_sma_amean',
        'shimmerLocal_sma_stddev', 'F0final__Turn_numOnsets',
        'F0final__Turn_duration']]], axis=1)
    return df

def process_data_head(df):
    users = df.pop('users')
    for i, measure in enumerate(users):
        for j in measure.keys():
            df.loc[df.index == i, int(j)] = True
    for i, measure in enumerate(users):
        for j in measure.keys():
            df.loc[df.index == i, str(f"{j}-x")] = measure[j]['x']
            df.loc[df.index == i, str(f"{j}-y")] = measure[j]['y']
            df.loc[df.index == i, str(f"{j}-w")] = measure[j]['width']
            df.loc[df.index == i, str(f"{j}-h")] = measure[j]['height']
            df.loc[df.index == i, str(f"{j}-is_confirmed")] = measure[j]['is_confirmed']
            df.loc[df.index == i, str(f"{j}-is_tentative")] = measure[j]['is_tentative']
            df.loc[df.index == i, str(f"{j}-distanceToObservedUser")] = float(measure[j]['distance']) if measure[j]['distance'] is not None else None
            df.loc[df.index == i, str(f"{j}-ObservedUser")] = float(measure[j]['user_min_distance']) if measure[j]['user_min_distance'] is not None else None
    # try:
    #     df["1-ObservedUser"] = df["1-ObservedUser"].astype(float)
    # except KeyError:
    #     pass
    # try:
    #     df["2-ObservedUser"] = df["2-ObservedUser"].astype(float)
    # except KeyError:
    #     pass
    # try:
    #     df["3-ObservedUser"] = df["3-ObservedUser"].astype(float)
    # except KeyError:
    #     pass
    # try:
    #     df["4-ObservedUser"] = df["4-ObservedUser"].astype(float)
    # except KeyError:
    #     pass
    # try:
    #     df["5-ObservedUser"] = df["5-ObservedUser"].astype(float)
    # except KeyError:
    #     pass
    # try:
    #     df["6-ObservedUser"] = df["6-ObservedUser"].astype(float)
    # except KeyError:
    #     pass
    # try:
    #     df["7-ObservedUser"] = df["7-ObservedUser"].astype(float)
    # except KeyError:
    #     pass
    # try:
    #     df["8-ObservedUser"] = df["8-ObservedUser"].astype(float)
    # except KeyError:
    #     pass
    return df