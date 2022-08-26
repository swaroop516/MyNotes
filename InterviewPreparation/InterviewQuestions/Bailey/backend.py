import mysql.connector
from mysql.connector import Error


def member_details(member_id, game_id=None, month=None):
    """
    params member_id: Mandotory field
    params game_id: Optional field
    params month: Optional field
    """
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="******",
    database="weather_db"
    )
    db_conn = mydb.cursor()
    if game_id is None and month is None:
        query =  f"""
        SELECT MEMBER_ID,
                'ALL' AS GAME_ID,
                'ALL' AS MONTH,
                ROUND(SUM(WIN_AMOUNT), 2) AS TOTAL_WIN_AMOUNT,
                ROUND(SUM(WAGER_AMOUNT), 2) AS TOTAL_WAGER_AMOUNT,
                CAST(ROUND(SUM(NUMBER_OF_WAGERS), 2) AS CHAR) AS TOTAL_NUMBER_OF_WAGERS
        FROM REVENUE_ANALYSIS
        WHERE MEMBER_ID = {member_id}
        GROUP BY MEMBER_ID, 'ALL', 'ALL'
        """
    elif game_id is None and month is not None:
        query =  f"""
        SELECT MEMBER_ID,
                'ALL' AS GAME,
                ACTIVITY_YEAR_MONTH AS MONTH,
                ROUND(SUM(WIN_AMOUNT), 2) AS TOTAL_WIN_AMOUNT,
                ROUND(SUM(WAGER_AMOUNT), 2) AS TOTAL_WAGER_AMOUNT,
                CAST(ROUND(SUM(NUMBER_OF_WAGERS), 2) AS CHAR) AS TOTAL_NUMBER_OF_WAGERS
        FROM REVENUE_ANALYSIS
        WHERE MEMBER_ID = {member_id} AND ACTIVITY_YEAR_MONTH = {month}
        GROUP BY MEMBER_ID, 'ALL', ACTIVITY_YEAR_MONTH
        """
    elif game_id is not None and month is None:
        query =  f"""
        SELECT MEMBER_ID,
                GAME_ID AS GAME,
                'ALL' AS MONTH,
                ROUND(SUM(WIN_AMOUNT), 2) AS TOTAL_WIN_AMOUNT,
                ROUND(SUM(WAGER_AMOUNT), 2) AS TOTAL_WAGER_AMOUNT,
                CAST(ROUND(SUM(NUMBER_OF_WAGERS), 2) AS CHAR) AS TOTAL_NUMBER_OF_WAGERS
        FROM REVENUE_ANALYSIS
        WHERE MEMBER_ID = {member_id} AND GAME_ID = {game_id}
        GROUP BY MEMBER_ID, GAME_ID, 'ALL'
        """
    elif game_id is not None and month is not None:
        query =  f"""
        SELECT MEMBER_ID,
                GAME_ID AS GAME,
                ACTIVITY_YEAR_MONTH AS MONTH,
                ROUND(SUM(WIN_AMOUNT), 2) AS TOTAL_WIN_AMOUNT,
                ROUND(SUM(WAGER_AMOUNT), 2) AS TOTAL_WAGER_AMOUNT,
                CAST(ROUND(SUM(NUMBER_OF_WAGERS), 2) AS CHAR) AS TOTAL_NUMBER_OF_WAGERS
        FROM REVENUE_ANALYSIS
        WHERE MEMBER_ID = {member_id} AND GAME_ID = {game_id} AND ACTIVITY_YEAR_MONTH = {month}
        GROUP BY MEMBER_ID, GAME_ID, ACTIVITY_YEAR_MONTH
        """        
    db_conn.execute(query)
    result = db_conn.fetchall()
    return result

# if __name__ == '__main__':
#     member_details(1001, month=201701)