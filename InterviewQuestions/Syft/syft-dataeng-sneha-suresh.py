#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np 
import logging
import os
from datetime import date


def main():
    logging.info("Reading data frame from file")
    df = pd.read_csv("/Users/swaroop/MyNotes/InterviewQuestions/Syft/worker_activity.csv")
    logging.info(f"shape of input dataframe {df.shape}")
    df['Date'] = pd.to_datetime(df.Date)

    # To filter the records as of 2020-12-01
    df = df[df.Date<= '2020-12-01']

    #To compare the last worked date by worker
    df['Date_lagged'] = (df.sort_values(by=['Date'], ascending=True)
                        .groupby(['Worker', 'Employer', 'Role'])['Date'].shift(1))
    #To compare the last worked employer by worker
    df['Employer_lagged'] = (df.sort_values(by=['Date'], ascending=True)
                        .groupby(['Worker'])['Employer'].shift(1))
    #To compare the last worked role by worker
    df['Role_lagged'] = (df.sort_values(by=['Date'], ascending=True)
                        .groupby(['Worker', 'Employer'])['Role'].shift(1))


    #If worker has worked only once, by default worker will qualify all 3 requirements. To handle it, lagged columns will be same as the current columns
    df['Date_lagged'] = df.Date_lagged.combine_first(df.Date)
    df['Role_lagged'] = df.Role_lagged.combine_first(df.Role)
    df['Employer_lagged'] = df.Employer_lagged.combine_first(df.Employer)


    #To check the difference between the current one and last one
    df['ts_diff'] =(df.Date - df.Date_lagged).dt.days


    """
    If the time difference between last two is less than 6 then we consier valid_flag as 1, if not valid_flag is 0. 
    If the employer and last employer is same then valid_flag is 1 else valid_flag is 0,
    If the role and last role is same then valid_flag is 1 else valid_flag is 0,
    """
    df['valid_flag'] = np.select(
    [((df['ts_diff'] <= 6) & (df['Employer'] == df['Employer_lagged'])  & (df['Role'] == df['Role_lagged']))],
        [1],
        default=0)


    #Adding rownumber for each worked based on the Date descending order
    df['rownumber'] = df.sort_values(['Date'], ascending=[False])                      .groupby(['Worker'])                      .cumcount() + 1


    #To check the count of how many worked qualifed for all 3 requirements this row number will be used
    df['validflag_rn'] = df.sort_values(['Date'], ascending=[False])                      .groupby(['Worker', 'valid_flag'])                      .cumcount() + 1


    # If customer has passed all 3 requirements, filtering only those records
    df1 = df[(df.valid_flag==1) & (df.rownumber == df.validflag_rn)]



    # Fetching the counter of the worker
    df2 = df1.groupby(['Worker'], as_index=False).size().sort_values(by=['size'], ascending=False)
    # Renaming the column
    df2 = df2.rename(columns={"size": "counter"})

    logging.info(f"shape of output dataframe {df2.shape}")
    # Writing back to csv file
    df2.to_csv("/Users/swaroop/MyNotes/InterviewQuestions/Syft/result.csv", index=False)


if __name__ == "__main__":
    logging.basicConfig(filename=f'{os.path.basename(__file__)}_{date.today()}.log',level=logging.INFO,format='%(asctime)s:%(levelname)s:%(message)s')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)
    logger = logging.getLogger(__name__)    
    main()
