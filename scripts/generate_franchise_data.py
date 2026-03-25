"""
맛나국밥 가상 프랜차이즈 데이터 생성 스크립트
- stores: 20개 매장
- menu_items: 8개 메뉴 (설렁탕/갈비탕/도가니탕/수육/만두/공기밥/소주/맥주)
- daily_sales: 2025년 1~12월 일별 매장별 메뉴별 매출
- promotions: 6개 프로모션
- inventory: 월별 식자재 입출고/재고
"""

import sqlite3
import pandas as pd
import numpy as np
from pathlib import Path

np.random.seed(42)

DB_PATH = Path(__file__).parent.parent / "data" / "franchise.db"


def create_stores():
    """20개 매장 데이터 생성"""
    store_types = ["직영", "가맹"]

    districts = [
        ("서울", "강남구"), ("서울", "마포구"), ("서울", "종로구"), ("서울", "송파구"),
        ("서울", "영등포구"), ("서울", "강서구"), ("서울", "서초구"), ("서울", "노원구"),
        ("경기", "수원시"), ("경기", "성남시"), ("경기", "고양시"), ("경기", "용인시"),
        ("인천", "남동구"), ("인천", "부평구"),
        ("부산", "해운대구"), ("부산", "부산진구"), ("부산", "동래구"),
        ("대구", "수성구"), ("대구", "달서구"), ("대구", "중구"),
    ]

    stores = []
    for i, (region, district) in enumerate(districts, start=1):
        stores.append({
            "store_id": i,
            "store_name": f"맛나국밥 {district}점",
            "region": region,
            "district": district,
            "store_type": np.random.choice(store_types, p=[0.3, 0.7]),
            "open_date": (
                pd.Timestamp("2022-01-01") + pd.Timedelta(days=int(np.random.randint(0, 730)))
            ).strftime("%Y-%m-%d"),
            "seating_capacity": int(np.random.choice([30, 40, 50, 60])),
        })

    return pd.DataFrame(stores)


def create_menu_items():
    """8개 메뉴 데이터 생성"""
    items = [
        {"menu_id": 1, "menu_name": "설렁탕",  "category": "탕",   "price": 11000, "cost": 4500},
        {"menu_id": 2, "menu_name": "갈비탕",  "category": "탕",   "price": 14000, "cost": 6000},
        {"menu_id": 3, "menu_name": "도가니탕", "category": "탕",   "price": 15000, "cost": 6500},
        {"menu_id": 4, "menu_name": "수육",    "category": "안주",  "price": 28000, "cost": 11000},
        {"menu_id": 5, "menu_name": "만두",    "category": "사이드", "price": 7000,  "cost": 2500},
        {"menu_id": 6, "menu_name": "공기밥",  "category": "사이드", "price": 1000,  "cost": 300},
        {"menu_id": 7, "menu_name": "소주",    "category": "주류",  "price": 5000,  "cost": 1500},
        {"menu_id": 8, "menu_name": "맥주",    "category": "주류",  "price": 6000,  "cost": 2000},
    ]
    return pd.DataFrame(items)


def create_promotions():
    """6개 프로모션 데이터 생성"""
    promos = [
        {
            "promo_id": 1, "promo_name": "신년할인",
            "discount_type": "정률", "discount_value": 10,
            "start_date": "2025-01-01", "end_date": "2025-01-15",
            "target_menu_id": None,
        },
        {
            "promo_id": 2, "promo_name": "봄맞이1+1",
            "discount_type": "1+1", "discount_value": 0,
            "start_date": "2025-03-15", "end_date": "2025-04-15",
            "target_menu_id": 5,
        },
        {
            "promo_id": 3, "promo_name": "여름보양식",
            "discount_type": "정률", "discount_value": 15,
            "start_date": "2025-07-15", "end_date": "2025-08-15",
            "target_menu_id": 3,
        },
        {
            "promo_id": 4, "promo_name": "추석세트",
            "discount_type": "정액", "discount_value": 3000,
            "start_date": "2025-09-25", "end_date": "2025-10-10",
            "target_menu_id": 4,
        },
        {
            "promo_id": 5, "promo_name": "연말감사",
            "discount_type": "정률", "discount_value": 10,
            "start_date": "2025-12-20", "end_date": "2025-12-31",
            "target_menu_id": None,
        },
        {
            "promo_id": 6, "promo_name": "긴급재고소진",
            "discount_type": "정률", "discount_value": 20,
            "start_date": "2025-06-01", "end_date": "2025-06-07",
            "target_menu_id": 2,
        },
    ]
    return pd.DataFrame(promos)


def create_daily_sales(stores_df, menu_df):
    """일별 매출 데이터 생성 (2025년 1~12월)"""
    dates = pd.date_range("2025-01-01", "2025-12-31", freq="D")

    # 카테고리별 기본 주문량
    base_qty_by_category = {
        "탕":   20,
        "안주":  6,
        "사이드": 18,
        "주류":  10,
    }

    records = []
    for _, store in stores_df.iterrows():
        store_factor = np.random.uniform(0.7, 1.3)

        for date in dates:
            # 주말 +35%
            weekend_boost = 1.35 if date.dayofweek >= 5 else 1.0

            # 계절 효과: 겨울 탕류 +25%, 여름 탕류 -15%
            month = date.month
            if month in [12, 1, 2]:
                season = "winter"
            elif month in [7, 8]:
                season = "summer"
            else:
                season = "normal"

            for _, menu in menu_df.iterrows():
                base_qty = base_qty_by_category[menu["category"]]

                if season == "winter" and menu["category"] == "탕":
                    season_boost = 1.25
                elif season == "summer" and menu["category"] == "탕":
                    season_boost = 0.85
                elif season == "summer" and menu["category"] == "주류":
                    season_boost = 1.2
                else:
                    season_boost = 1.0

                qty = int(max(0, np.random.poisson(
                    base_qty * store_factor * weekend_boost * season_boost
                )))

                if qty > 0:
                    records.append({
                        "store_id": store["store_id"],
                        "menu_id": menu["menu_id"],
                        "sale_date": date.strftime("%Y-%m-%d"),
                        "quantity": qty,
                        "total_amount": qty * menu["price"],
                    })

    return pd.DataFrame(records)


def create_inventory(stores_df):
    """월별 식자재 입출고/재고 데이터 생성"""
    ingredients = [
        ("사골",  "kg",  8000),
        ("양지",  "kg", 12000),
        ("갈비",  "kg", 25000),
        ("도가니", "kg", 18000),
        ("만두피", "kg",  4000),
        ("쌀",   "kg",  3000),
    ]

    records = []
    inv_id = 1
    months = [f"2025-{m:02d}" for m in range(1, 13)]

    for _, store in stores_df.iterrows():
        for ingredient, unit, unit_price in ingredients:
            opening = int(np.random.uniform(80, 150))

            for ym in months:
                month_num = int(ym.split("-")[1])

                # 계절별 사용량 조정
                if month_num in [12, 1, 2] and ingredient in ("사골", "양지", "도가니"):
                    usage_factor = 1.3
                elif month_num in [7, 8] and ingredient in ("사골", "양지", "도가니"):
                    usage_factor = 0.8
                else:
                    usage_factor = 1.0

                used = int(np.random.uniform(30, 60) * usage_factor)
                purchased = int(np.random.uniform(40, 80))
                closing = max(0, opening + purchased - used)

                records.append({
                    "inventory_id": inv_id,
                    "store_id": store["store_id"],
                    "ingredient_name": ingredient,
                    "unit": unit,
                    "unit_price": unit_price,
                    "year_month": ym,
                    "opening_stock": opening,
                    "stock_in": purchased,
                    "stock_out": used,
                    "closing_stock": closing,
                })
                inv_id += 1
                opening = closing

    return pd.DataFrame(records)


def save_to_sqlite(stores, menu, sales, promos, inventory):
    """SQLite에 저장"""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)

    stores.to_sql("stores", conn, if_exists="replace", index=False)
    menu.to_sql("menu_items", conn, if_exists="replace", index=False)
    sales.to_sql("daily_sales", conn, if_exists="replace", index=False)
    promos.to_sql("promotions", conn, if_exists="replace", index=False)
    inventory.to_sql("inventory", conn, if_exists="replace", index=False)

    conn.close()
    print(f"DB 저장 완료: {DB_PATH}")


def main():
    print("1. 매장 데이터 생성...")
    stores = create_stores()
    print(f"   → stores: {len(stores)}건")

    print("2. 메뉴 데이터 생성...")
    menu = create_menu_items()
    print(f"   → menu_items: {len(menu)}건")

    print("3. 프로모션 데이터 생성...")
    promos = create_promotions()
    print(f"   → promotions: {len(promos)}건")

    print("4. 일별 매출 데이터 생성...")
    sales = create_daily_sales(stores, menu)
    print(f"   → daily_sales: {len(sales):,}건")

    print("5. 재고 데이터 생성...")
    inventory = create_inventory(stores)
    print(f"   → inventory: {len(inventory):,}건")

    print("6. SQLite 저장...")
    save_to_sqlite(stores, menu, sales, promos, inventory)

    print("\n=== 데이터 요약 ===")
    print(f"매장 수:      {len(stores)}")
    print(f"메뉴 수:      {len(menu)}")
    print(f"매출 레코드:  {len(sales):,}")
    print(f"프로모션:     {len(promos)}")
    print(f"재고 레코드:  {len(inventory):,}")


if __name__ == "__main__":
    main()
