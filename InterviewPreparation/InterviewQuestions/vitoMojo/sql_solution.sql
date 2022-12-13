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