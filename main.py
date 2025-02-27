from fastapi import FastAPI
from dotenv import load_dotenv

app = FastAPI()

# .env 파일 로드
load_dotenv()

# 기본 루트 경로
@app.get("/")
async def root():
    return {"message": "AI API 서버가 실행 중입니다."}

# 기업정보 가져오기
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from finance.stock_api import get_stock_info
from config.db_config import MySQLSelector

@app.get("/companies/stock-info/{company_id}")
async def get_company_stock_info(company_id: int):
    # 1. MySQL에서 기업 정보 가져오기
    company_info = MySQLSelector.get_company_info(company_id)
    
    if not company_info:
        raise HTTPException(status_code=404, detail="회사 정보를 찾을 수 없습니다.")
    
    try:
        # 2. 가져온 티커로 주식 정보 조회
        stock_info = get_stock_info(company_info["ticker"])
        
        # 3. 응답 데이터 구성
        response_data = {
            "company_name": company_info["company_name"],
            "ticker": company_info["ticker"],
            "trading_volume": stock_info["trading_volume"],
            "trading_value": stock_info["trading_value"],
            "low_52weeks": stock_info["low_52weeks"],
            "high_52weeks": stock_info["high_52weeks"],
            "change_amount": stock_info["change_amount"],
            "change_percent": stock_info["change_percent"]
        }
        
        return response_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"주식 정보 조회 중 오류: {str(e)}")