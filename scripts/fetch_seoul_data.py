"""
서울 열린데이터광장 API 수집 스크립트
- 추정매출 (상권): OA-15572
- 점포 (상권): OA-15568
- 유동인구 (상권): OA-15569
"""

import requests
import sqlite3
import pandas as pd
from pathlib import Path
import time

API_KEY = "774672634373796e36334379464346"
BASE_URL = f"http://openapi.seoul.go.kr:8088/{API_KEY}/json"
DB_PATH = Path(__file__).parent.parent / "data" / "seoul_commercial.db"


def fetch_api(service_name, start=1, end=1000):
    """서울 열린데이터광장 API 호출 (페이징)"""
    all_rows = []
    idx = start

    while True:
        url = f"{BASE_URL}/{service_name}/{idx}/{idx + end - 1}/"
        print(f"  요청: {service_name} [{idx}~{idx + end - 1}]")

        try:
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            print(f"  ⚠ 요청 실패: {e}")
            break

        if service_name not in data:
            # 에러 응답 확인
            if "RESULT" in data:
                print(f"  ⚠ API 에러: {data['RESULT'].get('MESSAGE', 'unknown')}")
            break

        result = data[service_name]
        total = result.get("list_total_count", 0)
        rows = result.get("row", [])

        if not rows:
            break

        all_rows.extend(rows)
        print(f"  → {len(rows)}건 수집 (누적: {len(all_rows)}/{total})")

        if len(all_rows) >= total:
            break

        idx += end
        time.sleep(0.5)  # API 부하 방지

    return all_rows


def fetch_estimated_sales():
    """추정매출 데이터 (VwsmTrdarSelngQq)"""
    print("\n1. 추정매출 데이터 수집...")
    rows = fetch_api("VwsmTrdarSelngQq")
    if rows:
        df = pd.DataFrame(rows)
        print(f"   총 {len(df)}건 수집 완료")
        return df
    return pd.DataFrame()


def fetch_stores():
    """점포 데이터 (VwsmTrdarStorQq)"""
    print("\n2. 점포 데이터 수집...")
    rows = fetch_api("VwsmTrdarStorQq")
    if rows:
        df = pd.DataFrame(rows)
        print(f"   총 {len(df)}건 수집 완료")
        return df
    return pd.DataFrame()


def fetch_floating_pop():
    """유동인구 데이터 (VwsmTrdarFlpopQq)"""
    print("\n3. 유동인구 데이터 수집...")
    rows = fetch_api("VwsmTrdarFlpopQq")
    if rows:
        df = pd.DataFrame(rows)
        print(f"   총 {len(df)}건 수집 완료")
        return df
    return pd.DataFrame()


def save_to_sqlite(sales_df, stores_df, pop_df):
    """SQLite에 저장"""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)

    if not sales_df.empty:
        sales_df.to_sql("estimated_sales", conn, if_exists="replace", index=False)
        print(f"  → estimated_sales: {len(sales_df)}건 저장")

    if not stores_df.empty:
        stores_df.to_sql("stores", conn, if_exists="replace", index=False)
        print(f"  → stores: {len(stores_df)}건 저장")

    if not pop_df.empty:
        pop_df.to_sql("floating_population", conn, if_exists="replace", index=False)
        print(f"  → floating_population: {len(pop_df)}건 저장")

    conn.close()
    print(f"\nDB 저장 완료: {DB_PATH}")


def main():
    sales_df = fetch_estimated_sales()
    stores_df = fetch_stores()
    pop_df = fetch_floating_pop()

    print("\n4. SQLite 저장...")
    save_to_sqlite(sales_df, stores_df, pop_df)

    print("\n=== 수집 요약 ===")
    print(f"추정매출: {len(sales_df)}건")
    print(f"점포: {len(stores_df)}건")
    print(f"유동인구: {len(pop_df)}건")


if __name__ == "__main__":
    main()
