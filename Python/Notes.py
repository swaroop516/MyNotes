
#Converts dataframe to dictionary by grouping one column with values as list of employer
temp = df.groupby(['Worker']).apply(lambda x: x['Employer'].tolist()).to_dict()

#Converts dataframe to dictionary by grouping one column with values as dictionary of all other columns
temp_dict = df.groupby('ID').apply(lambda dfg: dfg.to_dict(orient='list')).to_dict()