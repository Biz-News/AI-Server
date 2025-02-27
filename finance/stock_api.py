from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime, timedelta
from pykrx import stock
import mysql.connector

app = FastAPI()

class StockRequest(BaseModel):
    company_id: int

def get_stock_info(company_id: int):
    try:
        # DB 연결 및 기업 ID로 기업명, 티커 조회
        conn = mysql.connector.connect(host='localhost', user='user', password='password', database='finance')
        cursor = conn.cursor()
        cursor.execute("SELECT company_name, ticker FROM companies WHERE company_id = %s", (company_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not result:
            return None

        company_name, ticker = result
        today = datetime.today()
        last_business_day = stock.get_nearest_business_day_in_a_week(today.strftime("%Y%m%d"))

        df = stock.get_market_ohlcv_by_date(last_business_day, last_business_day, ticker)
        if df.empty:
            return None

        volume = df.iloc[0]["거래량"]
        close_price = df.iloc[0]["종가"]
        open_price = df.iloc[0]["시가"]
        change_amount = close_price - open_price
        change_percent = round((change_amount / open_price) * 100, 2)

        start_52_weeks_ago = (today - timedelta(days=365)).strftime("%Y%m%d")
        df_52_weeks = stock.get_market_ohlcv_by_date(start_52_weeks_ago, last_business_day, ticker)
        high_52 = df_52_weeks["고가"].max()
        low_52 = df_52_weeks["저가"].min()

        return {
            "기업명": company_name,
            "티커": ticker,
            "거래량": volume,
            "52주 최저가": low_52,
            "52주 최고가": high_52,
            "전일 대비 등락 (원)": change_amount,
            "전일 대비 등락 (%)": change_percent,
        }
    except Exception as e:
        print(f"Error fetching stock data: {e}")
        return None