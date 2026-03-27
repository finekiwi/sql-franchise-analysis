```sql
/*──────────────────────────────────────────────────────────────────
  sql-franchise-analysis
  외식 프랜차이즈 시나리오 기반 SQL 분석 실습

  database  : franchise.db · seoul_commercial.db
  records   : daily_sales 58K · 서울 공공 상권 270만 건
  stack     : SQLite · Python · pandas · Jupyter
──────────────────────────────────────────────────────────────────*/
```

<br>

```sql
-- ================================================================
-- SCHEMA
-- ================================================================

CREATE TABLE stores (         -- 20개 매장 (직영 / 가맹)
    store_id        INTEGER PRIMARY KEY,
    store_name      TEXT,
    region          TEXT,
    district        TEXT,
    store_type      TEXT,
    open_date       TEXT,
    seating_capacity INTEGER
);

CREATE TABLE menu_items (     -- 8개 메뉴 (탕 / 안주 / 사이드 / 주류)
    menu_id   INTEGER PRIMARY KEY,
    menu_name TEXT,
    category  TEXT,
    price     INTEGER,
    cost      INTEGER
);

CREATE TABLE daily_sales (    -- 58,385건 · 2025년 전체
    store_id     INTEGER REFERENCES stores(store_id),
    menu_id      INTEGER REFERENCES menu_items(menu_id),
    sale_date    TEXT,
    quantity     INTEGER,
    total_amount INTEGER
);

CREATE TABLE promotions (     -- 6개 프로모션 (신년할인 ~ 긴급재고소진)
    promo_id       INTEGER PRIMARY KEY,
    promo_name     TEXT,
    discount_type  TEXT,
    discount_value INTEGER,
    start_date     TEXT,
    end_date       TEXT,
    target_menu_id INTEGER
);

CREATE TABLE inventory (      -- 1,440건 · 월별 식자재 입출고
    inventory_id  INTEGER PRIMARY KEY,
    store_id      INTEGER REFERENCES stores(store_id),
    ingredient_name TEXT,
    year_month    TEXT,
    opening_stock INTEGER,
    stock_in      INTEGER,
    stock_out     INTEGER,
    closing_stock INTEGER
);
```

<br>

```sql
-- ================================================================
-- QUERIES
-- ================================================================

-- 월별 매출 추이 (계절 효과 확인)
SELECT SUBSTR(sale_date, 1, 7) AS 월,
       SUM(total_amount)       AS 총매출
FROM daily_sales
GROUP BY 월
ORDER BY 월;
```

| 월 | 총매출 |
|---|---|
| 2025-01 | 1,009,678,000 |
| 2025-07 | 796,570,000 &nbsp;← 비수기 |
| 2025-12 | 1,005,456,000 |

<br>

```sql
-- 전체 평균보다 높은 매장 (서브쿼리)
SELECT store_name, SUM(total_amount) AS 총매출
FROM daily_sales
JOIN stores ON daily_sales.store_id = stores.store_id
GROUP BY store_name
HAVING 총매출 >= (
    SELECT AVG(총매출)
    FROM (
        SELECT SUM(total_amount) AS 총매출
        FROM daily_sales
        GROUP BY store_id
    ) AS sub
)
ORDER BY 총매출 DESC;
```

| store_name | 총매출 |
|---|---|
| 맛나국밥 영등포구점 | 654,547,000 |
| 맛나국밥 용인시점 | 629,635,000 |
| … 9개 매장 | > 평균 (532M) |

<br>

```sql
-- 매장 순위 + 직영 필터 (VIEW + 윈도우 함수)
CREATE VIEW v_store_sales AS
SELECT store_name, store_type, region,
       SUM(total_amount)                              AS 총매출,
       RANK() OVER (ORDER BY SUM(total_amount) DESC)  AS 순위
FROM daily_sales
JOIN stores ON daily_sales.store_id = stores.store_id
GROUP BY store_name, store_type, region;

SELECT store_name, region, 총매출, 순위
FROM   v_store_sales
WHERE  store_type = '직영'
ORDER BY 순위;
```

| store_name | region | 총매출 | 순위 |
|---|---|---|---|
| 맛나국밥 영등포구점 | 서울 | 654,547,000 | 1 |
| 맛나국밥 달서구점 | 대구 | 601,874,000 | 5 |
| 맛나국밥 강서구점 | 서울 | 589,305,000 | 6 |
| 맛나국밥 성남시점 | 경기 | 414,822,000 | 20 |

<br>

```sql
-- ================================================================
-- FILES
-- ================================================================

SELECT path, description FROM project_files ORDER BY phase;

-- path                                   description
-- scripts/generate_franchise_data.py  -- 가상 데이터 생성 및 SQLite 적재
-- scripts/fetch_seoul_data.py         -- 서울 열린데이터광장 API 수집
-- queries/phase2_basic_queries.sql    -- SELECT · WHERE · JOIN · GROUP BY
-- queries/phase3_analysis_queries.sql -- HAVING · 서브쿼리 · 윈도우 함수
-- queries/phase4_view_queries.sql     -- VIEW · 데이터마트
-- notebooks/phase2_basic.ipynb
-- notebooks/phase3_analysis.ipynb
-- notebooks/phase4_view.ipynb
-- data/                               -- gitignored

-- ================================================================
-- PHASES
-- ================================================================

SELECT 1 AS phase, 'ERD 설계 · 가상 데이터 생성 · SQLite 적재'          AS covered;
SELECT 2 AS phase, 'SELECT · WHERE · ORDER BY · GROUP BY · JOIN'         AS covered;
SELECT 3 AS phase, 'HAVING · subquery · window function (RANK)'          AS covered;
SELECT 4 AS phase, 'CREATE VIEW · data mart'                             AS covered;
```
