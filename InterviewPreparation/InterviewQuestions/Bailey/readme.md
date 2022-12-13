SQL-
1. Code is written in MySQL. However we can port to other databases easily.
2. I have added the filter condition of 201701 to 201806 from calendar table, just to limit for this period. We can also remove this filter, code will work perfectly.
3. sql-1001-out is the output of the member 1001 is in Results folder.
4. sql-1002-out is the output of the member 1002 is in Results folder.
5. For 1003, there is no output, he has not used any real money. So it got filtered out. 
6. As the data could be very huge with 10M+, I have optimised to not to use any self joins.
7. I have also added few data with edge cases to test the sql query.


Rest API
Steps to follow for deployment-
1. Data should be loaded in any database. Here I have loaded to mysql DB.
2. Install the modules used for this by pip install -r requirements.txt
3. I have bulit the rest api using flask frame work in python.
4. I have also handled member_id as mandatory field  and game_id, month as optional parameters.
5. To deploy in local host, we need to clone this folder and launch the application by python app.py.
6. To deploy in server we need to given an end point of the server and launch the app.py in server. We can use Tomcat or Nginix for server side deployment.
7. If no data is recieved from database, it will show as no data found for member.
8. Screenshots of few api calls from the web page are added in the Results folder.


Rest API Tests done-
1. If member id is not passed, it will remind the customer as member_id is mandatory.
2. If game_id is passed along with member id it will give relavant details. Similarly to month field also. If all three are passed it will give the respective details.


