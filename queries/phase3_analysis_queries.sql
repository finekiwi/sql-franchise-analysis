-- Phase 3: 분석 쿼리 (HAVING / 서브쿼리 / 윈도우 함수)
-- DB: data/franchise.db


-- ============================================================
-- 1. HAVING
-- ============================================================

-- 3-1. 연간 총매출 5.5억 이상 매장만 조회
SELECT store_name, SUM(total_amount) AS 총매출
FROM daily_sales
JOIN stores ON daily_sales.store_id = stores.store_id
GROUP BY store_name
HAVING SUM(total_amount) >= 550000000
ORDER BY 총매출 DESC;

-- 3-2. 카테고리별 평균 판매수량이 15 이상인 카테고리만 조회
SELECT category, AVG(quantity) AS 평균수량
FROM daily_sales
JOIN menu_items ON daily_sales.menu_id = menu_items.menu_id
GROUP BY category
HAVING AVG(quantity) >= 15
ORDER BY 평균수량 DESC;


-- ============================================================
-- 2. 서브쿼리
-- ============================================================

-- 3-3. 전체 평균 매출보다 높은 매장만 조회
SELECT store_name, SUM(total_amount) AS 총매출
FROM daily_sales
JOIN stores ON daily_sales.store_id = stores.store_id
GROUP BY store_name
HAVING 총매출 >= (
    SELECT AVG(총매출)
    FROM (
        SELECT store_name, SUM(total_amount) AS 총매출
        FROM daily_sales
        JOIN stores ON daily_sales.store_id = stores.store_id
        GROUP BY store_name
    ) AS sub
)
ORDER BY 총매출 DESC;


-- ============================================================
-- 3. 윈도우 함수
-- ============================================================

-- 3-4. 매장별 총매출 순위 (RANK)
SELECT
    store_name,
    SUM(total_amount) AS 총매출,
    RANK() OVER (ORDER BY SUM(total_amount) DESC) AS 순위
FROM daily_sales
JOIN stores ON daily_sales.store_id = stores.store_id
GROUP BY store_name
ORDER BY 총매출 DESC;
