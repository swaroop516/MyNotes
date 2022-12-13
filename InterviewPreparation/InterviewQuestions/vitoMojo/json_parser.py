"""
This script takes json file as input and flattens it and writes to database.
"""
import json 
import pandas as pd 
import sqlalchemy
import logging
from datetime import date

file_path = "/Users/swaroop/Downloads/"

log = logging.getLogger() 
log.setLevel(logging.INFO) 

def flatten_json(df):
    df.columns = [col.replace('.', '_') for col in df.columns]
    all_cols = df.columns
    for col in all_cols:
        if type(df[col][0]) == list:
            df = df.explode(col)
            df = df.reset_index().drop(['index'], axis=1)
        elif type(df[col][0]) == dict:
            temp_df = pd.json_normalize(df[col])
            new_cols = [f'{col}_{e_col}' for e_col in temp_df.columns]
            temp_df.columns = new_cols
            df = pd.concat([df.drop(col, axis=1), temp_df], axis=1)
    logging.info(f"Flatten the Json")
    return df

def db_write(df, table_name, mode):
    database_username = 'root'
    database_password = '*******'
    database_ip       = 'localhost'
    database_name     = 'weather_db'
    database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                                   format(database_username, database_password, 
                                                          database_ip, database_name))
    df.to_sql(con=database_connection, name=table_name, if_exists=mode)
    logging.info(f"Written the dataframe to Database")

def main():
    logging.info(f"Reading the json data from {file_path}")
    with open(f"{file_path}/task_data.json") as f:
        d = json.load(f)
    norm_df = pd.json_normalize(d)
    nested_level = 4
    for i in range(0,nested_level):
        norm_df = flatten_json(norm_df)
    db_write(norm_df, table_name='orders_stg', mode='replace')    


if __name__ == "__main__":
    main()
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',    
                        level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S', filename=f'flatten_{date.today()}.log', force=True)    
