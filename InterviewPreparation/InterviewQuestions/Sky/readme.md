This code will calculate the total bill of each user for the given dataset.
1. Code is written in python with version 3.9.7, using inbuilt libraries.

Assumptions,
1. Metadata of the file will not change.
2. Assumed length of the fields for data validation as in the given data.

Code explanation-
1. Code is implemeted in Object Oriented Programming approach.
2. 3 classes have been defined,
    File_handling - Which has the functions to read, validate and write the file
    Billing - Which has functions to calculate the cost based on seconds, promotional discount, final bill
    Utility - This class has helper functions. In this case, custom_group_by.
3. Final outcome will be saved in Result.csv

Execution-
1. This code can be executed on any python IDE.
2. Change the file path in variable "folder" in Sky.py.
3. Execute using command "python Sky.py"

I have written the code using python native modules. I can also implement the same using other modules that are available in python that can be used to perform the given transformations at table level like pandas.
