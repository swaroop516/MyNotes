import numpy as np
import pandas as pd
from datetime import date
import logging
import os


def continuity_counter(flag_list):
    """
    flag_list: list of valid and invalid flags for each worker
    """
    # list has recieved based on the dates worked in decsending order, so reversing it
    flag_list = flag_list[::-1]
    count = 1
    for i in range(0, len(flag_list)):
        if flag_list[i] == 1:
            count = 0 # if valid flag is 1 then reset the counter to 0
        else:
            count = count + 1
    return count


def rule_check(df, report_date):
    """
    df: input data frame
    report_date: report fetching date.
    """

    df = df[df.Date <= report_date]
    #To compare the next working date by worker
    df['Date_lead'] = (df.sort_values(by=['Date'], ascending=False)
                        .groupby(['Worker', 'Employer', 'Role'])['Date'].shift(1))
    #To compare the next working date employer by worker
    df['Employer_lead'] = (df.sort_values(by=['Date'], ascending=False)
                        .groupby(['Worker'])['Employer'].shift(1))
    #To compare the next working date role by worker
    df['Role_lead'] = (df.sort_values(by=['Date'], ascending=False)
                        .groupby(['Worker', 'Employer'])['Role'].shift(1))
    # For the last record of worker, adding the report date to check the number of days to report date
    df['Date_lead'] = df['Date_lead'].fillna(report_date)
    # For the last record of worker, adding the role
    df['Role_lead'] = df.Role_lead.combine_first(df.Role)
    # For the last record of worker, adding the employer
    df['Employer_lead'] = df.Employer_lead.combine_first(df.Employer)    
    # to check the difference between days
    df['ts_diff'] =(df.Date_lead - df.Date).dt.days
    
    # If the time difference between last two is less than 6 then we consier valid_flag as 0, if not valid_flag is 1. 
    # If the employer and last employer is same then valid_flag is 0 else valid_flag is 1,
    # If the role and last role is same then valid_flag is 0 else valid_flag is 1,
        
    df['valid_flag'] = np.where(((df['ts_diff'] <= 6) & 
                                (df['Employer'] == df['Employer_lead']) &
                                (df['Role'] == df['Role_lead']))
                                ,0 ,1)
    # Grouping the valid flag based on worker, to make the countinuity 0 based on the 3 conditions
    df = df.groupby('Worker')['valid_flag'].apply(list).reset_index(name="Valid_flag")
    # applying function defined for continuity checker
    df['Continuity'] = df.apply(lambda row : continuity_counter(row['Valid_flag']), axis = 1)
    df = df.loc[df['Continuity']>0,['Worker', 'Continuity']]
    df = df.sort_values(by='Continuity', ascending=False)
    return df

def main():
    logging.info("Reading data frame from file")
    
    file_path = "/Users/swaroop/MyNotes/InterviewPreparation/InterviewQuestions/Syft/"
    
    df = pd.read_csv(f"{file_path}worker_activity.csv")
    
    logging.info(f"shape of input dataframe {df.shape}")
    
    df['Date'] = pd.to_datetime(df.Date)
    result_df = rule_check(df, '2021-12-01 00:00:00')

    
    logging.info(f"shape of output dataframe {result_df.shape}")
    # Writing back to csv file
    result_df.to_csv(f"{file_path}result.csv", index=False)


if __name__ == "__main__":
    # Below code will help in logging the execution
    logging.basicConfig(filename=f'{os.path.basename(__file__)}_{date.today()}.log',level=logging.INFO,format='%(asctime)s:%(levelname)s:%(message)s')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    logger = logging.getLogger(__name__)    
    # Functionality is written in main function
    main()