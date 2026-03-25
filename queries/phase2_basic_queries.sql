-- Phase 2: 기본 쿼리 (SELECT / WHERE / ORDER BY / GROUP BY / JOIN)
-- DB: data/franchise.db


-- ============================================================
-- 1. 단일 테이블 조회 (SELECT / WHERE / ORDER BY)
-- ============================================================

-- 1-1. 가맹점만 조회 (좌석수 내림차순)
SELECT store_name, region, store_type, seating_capacity
FROM stores
WHERE store_type = '가맹'
ORDER BY seating_capacity DESC;

-- 1-2. 가격 10,000원 이상 메뉴 조회 (가격 오름차순)
SELECT menu_name, category, price, cost
FROM menu_items
WHERE price >= 10000
ORDER BY price ASC;


-- ============================================================
-- 2. GROUP BY 집계
-- ============================================================

-- 2-1. 매장별 총 매출액 (내림차순)
SELECT store_id, SUM(total_amount) AS 총매출
FROM daily_sales
GROUP BY store_id
ORDER BY 총매출 DESC;

-- 2-2. 메뉴별 총 판매수량 및 총 매출액 (수량 내림차순)
SELECT menu_id, SUM(quantity) AS 총수량, SUM(total_amount) AS 총매출
FROM daily_sales
GROUP BY menu_id
ORDER BY 총수량 DESC;

-- 2-3. 월별 총 매출액 (월 오름차순)
SELECT SUBSTR(sale_date, 1, 7) AS 월, SUM(total_amount) AS 총매출
FROM daily_sales
GROUP BY 월
ORDER BY 월 ASC;


-- ============================================================
-- 3. 2테이블 JOIN
-- ============================================================

-- 3-1. 매장 이름별 총 매출액 (daily_sales × stores)
SELECT store_name, SUM(total_amount) AS 총매출
FROM daily_sales
JOIN stores ON daily_sales.store_id = stores.store_id
GROUP BY store_name
ORDER BY 총매출 DESC;

-- 3-2. 메뉴 이름별 총 판매수량 및 총 매출액 (daily_sales × menu_items)
SELECT menu_name, category, SUM(quantity) AS 총수량, SUM(total_amount) AS 총매출
FROM daily_sales
JOIN menu_items ON daily_sales.menu_id = menu_items.menu_id
GROUP BY menu_name
ORDER BY 총매출 DESC;


-- ============================================================
-- 4. 3테이블 JOIN + GROUP BY
-- ============================================================

-- 4-1. 지역별 카테고리별 총 매출액 (daily_sales × stores × menu_items)
SELECT region, category, SUM(total_amount) AS 총매출
FROM daily_sales
JOIN stores     ON daily_sales.store_id = stores.store_id
JOIN menu_items ON daily_sales.menu_id  = menu_items.menu_id
GROUP BY region, category
ORDER BY 총매출 DESC;
