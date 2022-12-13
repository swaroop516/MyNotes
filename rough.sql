-- Active: 1653296915051@@127.0.0.1@3306@weather_db
--select distinct bundles.kitchenStation from orders_stg;



CREATE TABLE USER_ORDER AS (
	SELECT DISTINCT createdAt,
	extStoreUUID,
	extTenantUUID,
	requestedFrom,
	STATUS,
	takeaway,
	timezone,
	updatedAt,
	uuid,
	user_extUserUUID AS extUserUUID,
	bundles_basketUUID AS bundlesUUID FROM ORDERS_STG
	);

CREATE TABLE bundles AS (
	SELECT DISTINCT bundles_basketUUID AS basketUUID,
	bundles_description AS description,
	bundles_discount AS discount,
	bundles_menuUUID AS menuUUID,
	bundles_name AS name,
	bundles_status AS STATUS,
	bundles_subtotalAmount AS subtotalAmount,
	bundles_totalAmount AS totalAmount,
	bundles_uuid AS uuid,
	bundles_vatAmount AS vatAmount,
	bundles_vatRateEatIn AS vatRateEatIn,
	bundles_vatRateTakeaway AS vatRateTakeaway,
	bundles_category_name AS category_name,
	bundles_category_uuid AS category_uuid,
	bundles_kitchenStation_extTenantUUID AS kitchenStation_extTenantUUID,
	bundles_kitchenStation_name AS kitchenStation_name,
	bundles_kitchenStation_uuid AS kitchenStation_uuid,
	bundles_kitchenStation AS kitchenStation,
	bundles_promotion_uuid AS promotion_uuid,
	bundles_promotion_value AS promotion_value,
	bundles_itemTypes_uuid AS itemTypes_uuid FROM ORDERS_STG
	);

CREATE TABLE ITEMTYPES AS (
	SELECT DISTINCT bundles_itemTypes_name AS name,
	bundles_itemTypes_uuid AS uuid,
	bundles_itemTypes_items_discount AS discount,
	bundles_itemTypes_items_itemUUID AS item_itemUUID,
	bundles_itemTypes_items_name AS itemname,
	bundles_itemTypes_items_subtotalAmount AS subtotalAmount,
	bundles_itemTypes_items_totalAmount AS totalAmount,
	bundles_itemTypes_items_type AS type,
	bundles_itemTypes_items_uuid AS item_uuid,
	bundles_itemTypes_items_vatAmount AS vatAmount,
	bundles_itemTypes_items_vatRateEatIn AS vatRateEatIn,
	bundles_itemTypes_items_vatRateTakeaway AS vatRateTakeaway FROM ORDERS_STG
	);

--How many total orders were there in the dataset?
SELECT COUNT(DISTINCT uuid)
FROM orders_stg;

--How many orders were from each channel
SELECT requestedFrom,
	COUNT(DISTINCT uuid)
FROM orders_stg
GROUP BY requestedFrom;

--How many items were sold for each hour of the day for each tenant?
SELECT HOUR(FROM_UNIXTIME(updatedAt / 1000)) AS HOUR,
	extTenantUUID AS extTenantUUID,
	COUNT(DISTINCT uuid)
FROM orders_stg
GROUP BY HOUR(FROM_UNIXTIME(updatedAt / 1000)),
	extTenantUUID;

--What were the top 5 items sold for each tenant?
SELECT * FROM
(SELECT *,
	COUNT(*) OVER(PARTITION BY extTenantUUID, bundles_itemTypes_items_itemUUID) AS count
FROM orders_stg) A
WHERE count>5;

---What were the items for each tenant that were sold more than 5 of?
SELECT extTenantUUID,
	bundles_itemTypes_items_itemUUID,
	COUNT(*)
FROM orders_stg
GROUP BY extTenantUUID,
	bundles_itemTypes_items_itemUUID
HAVING COUNT(*) > 5;

---Which order UUIDs had multiples of the same bundle?
SELECT uuid,
	bundles_uuid,
	count(*)
FROM orders_stg
GROUP BY uuid,
	bundles_uuid
HAVING count(*) > 1;

