"""
This script takes json file as input and flattens it and write back in json format.
"""
import pandas as pd
import logging
from datetime import date

file_path = "/Users/swaroop/Downloads/"

log = logging.getLogger() 
log.setLevel(logging.INFO) 

def flatten_dict(df, col):
    """
    params df: Input dataframe
    params col: dictionry column to flat
    """
    df = pd.concat([df.drop([col], axis=1), df[col].apply(pd.Series)], axis=1)
    return df

def main():
    logging.info(f"Reading the json file from {file_path}")
    df = pd.read_json(f"{file_path}python-test-file.json")
    df = df.explode('data')  #Explode list to multiple rows
    df = flatten_dict(df, 'data') #Explode dictionary to multiple columns
    df = flatten_dict(df, 'temp') #Explode dictionary to multiple columns
    df['loaddate'] = str(date.today()) #Adding the today's date for loaddate
    df = df.reset_index().drop(['index'], axis=1) #Removing the index
    df.to_json(f"{file_path}python-out-file.json")
    logging.info(f"Written the flatten json file to {file_path}")


if __name__ == "__main__":
    main()
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',    
                        level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S', filename=f'flatten_{date.today()}.log', force=True)    
