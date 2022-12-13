This code will generate the report of the workers based on the given conditions
1. Code is written in python version 3.9.7. And pandas version 1.4.2.

Code explanation-
1. Code has 2 functions,
    rule_check - Here it checks the worker has below 3 behaviour.
        A worker had no activity for more than 6 days.
        A worker stayed active but switched to a different employer.
        A worker stayed active but switched to a different role.
    If any row of the worker has seen this case then the flag is set as 1 else as 0.
    
    continuity-counter - Based on the flag in rule_check function, if flag is 1 counter is reset to 0, else it increments.
2. report_date has passed in function, which can be altered based on required date.

Answers for Open Questions-
1. Time complexity is linear.
2. In production environment it is good to have columnar database. Reason being, for analytics columnar database works faster for execution. Good to maintain data in sharded.
3. For the large scale application, it is good to be in lakehouse environment which will help in reducing the cost, fast in execution, easy to integrate to other platforms like machine learning, BI.
