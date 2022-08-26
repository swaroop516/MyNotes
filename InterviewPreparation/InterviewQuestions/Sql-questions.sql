-- Active: 1653296915051@@127.0.0.1@3306@weather_db
WITH JOR AS (
    SELECT 'DELHI' AS SRC, 'MUM' AS DEST UNION
    SELECT 'MUM' AS SRC, 'DELHI' AS DEST UNION
    SELECT 'DELHI' AS SRC, 'KOLKATA' AS DEST UNION
    SELECT 'KOLKATA' AS SRC, 'DELHI' AS DEST UNION
    SELECT 'MUM' AS SRC, 'NAGPUR' AS DEST 
)SELECT A.*, B.* FROM JOR A LEFT JOIN JOR B
ON A.SRC = B.DEST
AND A.DEST = B.SRC ;