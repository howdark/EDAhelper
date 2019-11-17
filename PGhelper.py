import psycopg2 as pg
import yaml
import pandas as pd
import numpy as np

"""
Initialize PostgreSQL DB Connection
"""
def db_init():
    conn = pg.connect(host='172.21.0.3', database='openmarket', user='dev', password='qwerasdf')
    cursor = conn.cursor() 
    return conn, cursor


"""
Close PostgreSQL DB Connection
"""
def db_close(conn, cursor):
    cursor.close()
    conn.close()
    return


"""
"""
def param_load(file):
    with open(file, 'r') as f:
        params = yaml.load(f, Loader=yaml.Loader)
    return params

"""
"""
def feature_info_load(file):
    with open(file, 'r') as f:
        feature_info = yaml.load(f, Loader=yaml.Loader)
    return feature_info
"""
"""
def feature_info_dump(data, file):
    with open(file, 'w') as f:
        yaml.dump(data, f, Dumper=yaml.Dumper)
    return

"""
Add file_path to feature_group in feature_info

    - feature_info : dict type. key is feature_group and values are file_paths.
    - feature_group : kinds of tag group
    - file_path : feature_group에 해당하는 data 파일 경로
"""
def feature_info_update(feature_info, feature_group, file_path):
    try:
        if type(feature_info[feature_group]) == list:
            dup_check = 0
            
            for path in feature_info[feature_group]:
                if file_path == path:
                    dup_check += 1
            if dup_check == 0:                
                feature_info[feature_group] = feature_info[feature_group] + [file_path]
            else:
                print("File_path is duplicated. Please check file path")
                return feature_info, dup_check
        else:
            feature_info[feature_group] = [feature_info[feature_group]] + [file_path]
    except:
        dup_check = 0
        feature_info[feature_group] = [file_path]
    
    return feature_info, dup_check


"""
save_file
"""
def save_with_feature_group(df, file_path, feature_info_path, feature_group):
    print('Updating feature group.')
    try:        
        feature_info = feature_info_load(feature_info_path)
    except:
        feature_info = dict()

    feature_info, dup_check = feature_info_update(feature_info, feature_group, file_path)
    
    if dup_check == 0:
        with open(feature_info_path, 'w') as f:
            yaml.dump(feature_info, f, Dumper=yaml.Dumper)
        print('-- Done.')   

        print('Saving data to {}'.format(file_path))
        df.to_csv(file_path, index=False)
        print('-- Done.')    
    
    return


"""
"""
def load_feature_group(feature_group, feature_info):
    file_path = feature_info[feature_group][0]
    df = pd.read_csv(file_path)
    df_dict = {'cols': list(df.columns), 'shape': df.shape}
    return df, df_dict


"""
"""
def transform_recom(df, numeric_cols, log_skew_threshold=1.0):
    rslt = df[numeric_cols].describe().apply(lambda x: 3*(x['mean'] - x['50%'])/x['std'])
    log_trns_cols = list(rslt[rslt > 1.0].index)
    sqrt_trns_cols = list(rslt[rslt < -1.0].index)
    normal_cols = list(set(rslt.index) - set(log_trns_cols) - set(sqrt_trns_cols))
    
    return normal_cols, log_trns_cols, sqrt_trns_cols
    

"""
"""
def log_transform(df, log_trns_cols):
    df[log_trns_cols] = df[log_trns_cols].apply(lambda x: np.log1p(x), axis=1)
    return df


"""
"""
def sqrt_transform(df, sqrt_trns_cols):
    df[sqrt_trns_cols] = df[sqrt_trns_cols].apply(lambda x: np.sqrt(x), axis=1)
    return df