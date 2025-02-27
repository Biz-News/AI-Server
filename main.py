from fastapi import FastAPI, HTTPException
from finance.stock_api import get_stock_info
from app.DB import DB
from dotenv import load_dotenv

app = FastAPI()
db = DB()  # DB 클래스 인스턴스 생성

# .env 파일 로드
load_dotenv()

# 기본 루트 경로
@app.get("/")
async def root():
    return {"message": "AI API 서버가 실행 중입니다."}

# 기업정보 가져오기
@app.get("/companies/stock-info/{company_id}")
async def get_company_stock_info(company_id: str):
    # 1. MySQL에서 기업 정보 가져오기
    company_info = db.get_company_info(company_id)
    if not company_info:
        raise HTTPException(status_code=404, detail="회사 정보를 찾을 수 없습니다.")
    
    try:
        # ticker 필드가 없거나 null인 경우 처리
        if "ticker" not in company_info or not company_info["ticker"]:
            raise HTTPException(status_code=404, detail="해당 기업의 종목코드(ticker) 정보가 없습니다.")
        
        # 2. 가져온 티커로 주식 정보 조회
        stock_info = get_stock_info(company_info["ticker"])
        
        # 3. 응답 데이터 구성
        response_data = {
            "company_name": company_info.get("company", "정보 없음"),
            "ticker": company_info.get("ticker", "정보 없음"),
            "trading_volume": stock_info.get("trading_volume", 0),
            "trading_value": stock_info.get("trading_value", 0),
            "low_52weeks": stock_info.get("low_52weeks", 0),
            "high_52weeks": stock_info.get("high_52weeks", 0),
            "change_amount": stock_info.get("change_amount", 0),
            "change_percent": stock_info.get("change_percent", 0.0),
        }
        return response_data
    
    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"주식 정보 조회 중 오류: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
