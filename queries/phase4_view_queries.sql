-- Phase 4: VIEW + 데이터마트
-- DB: data/franchise.db
-- 주의: VIEW가 이미 존재하면 DROP 후 재생성


-- ============================================================
-- 1. VIEW 생성
-- ============================================================

-- 4-1. 매장별 총매출 + 순위 VIEW
DROP VIEW IF EXISTS v_store_sales;
CREATE VIEW v_store_sales AS
SELECT
    region,
    store_type,
    store_name,
    SUM(total_amount) AS 총매출,
    RANK() OVER (ORDER BY SUM(total_amount) DESC) AS 순위
FROM daily_sales
JOIN stores ON daily_sales.store_id = stores.store_id
GROUP BY store_name, region, store_type
ORDER BY 총매출 DESC;


-- 4-3. 월별 카테고리별 매출 VIEW
DROP VIEW IF EXISTS v_monthly_category_sales;
CREATE VIEW v_monthly_category_sales AS
SELECT
    category,
    SUBSTR(sale_date, 1, 7) AS 월,
    SUM(total_amount) AS 총매출,
    SUM(quantity) AS 총수량
FROM daily_sales
JOIN menu_items ON daily_sales.menu_id = menu_items.menu_id
GROUP BY 월, category
ORDER BY 월, category;


-- ============================================================
-- 2. VIEW 활용
-- ============================================================

-- 4-2. v_store_sales에서 직영점만 조회
SELECT store_name, region, 총매출, 순위
FROM v_store_sales
WHERE store_type = '직영'
ORDER BY 순위;

-- 월별 탕 카테고리 매출 추이
SELECT 월, 총매출, 총수량
FROM v_monthly_category_sales
WHERE category = '탕'
ORDER BY 월;
