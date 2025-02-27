from datetime import datetime, timedelta
from pykrx import stock

def get_stock_info(ticker):
    """
    주어진 티커(종목코드)에 대한 주식 정보를 가져옵니다.
    """
    try:
        if not ticker:
            raise ValueError("티커 정보가 없습니다.")
            
        # 오늘 날짜 기준 최근 영업일 가져오기
        today = datetime.today()
        last_business_day = stock.get_nearest_business_day_in_a_week(today.strftime("%Y%m%d"))
        
        # 거래량, 종가 등 데이터 가져오기
        df = stock.get_market_ohlcv_by_date(last_business_day, last_business_day, ticker)
        
        if df.empty:
            raise ValueError(f"티커 {ticker}에 대한 데이터가 없습니다.")
        
        # 당일 거래 정보
        volume = int(df.iloc[0]["거래량"])
        close_price = int(df.iloc[0]["종가"])
        open_price = int(df.iloc[0]["시가"])
        
        # 거래대금 (거래량 * 종가) - 간소화된 계산
        trading_value = int(volume * close_price)
        
        # 52주 최고가 및 최저가 조회
        start_52_weeks_ago = (today - timedelta(days=365)).strftime("%Y%m%d")
        df_52_weeks = stock.get_market_ohlcv_by_date(start_52_weeks_ago, last_business_day, ticker)
        high_52 = int(df_52_weeks["고가"].max())
        low_52 = int(df_52_weeks["저가"].min())
        
        # 전일 대비 등락 계산
        change_amount = close_price - open_price
        change_percent = round((change_amount / open_price) * 100, 2)
        
        # 결과 반환
        return {
            "trading_volume": volume,
            "trading_value": trading_value,
            "low_52weeks": low_52,
            "high_52weeks": high_52,
            "change_amount": change_amount,
            "change_percent": change_percent
        }
        
    except Exception as e:
        print(f"주식 정보 조회 중 오류 발생: {str(e)}")
        raise ValueError(f"주식 정보 조회 실패: {str(e)}")