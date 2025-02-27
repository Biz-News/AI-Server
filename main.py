from fastapi import FastAPI
from dotenv import load_dotenv

app = FastAPI()

# .env 파일 로드
load_dotenv()

from app.model import SingleResponseModel
from app.raw import keywords_filtering_prompt_text, summary_prompt_text

from test.test_news import news
from test.test_keywords import keywords


keywords_filtering_model = SingleResponseModel(keywords_filtering_prompt_text)
summary_model = SingleResponseModel(summary_prompt_text)

# 기본 루트 경로
@app.get("/")
async def root():
    return {"message": "AI API 서버가 실행 중입니다."}

#@app.get("/company/{company}")
#async def get_company(company: str):
#    keywords = get_keywords()
#    return {"company": company}
@app.get("/company/{company}/keywords")
async def get_keywords_about_company(company: str):
    # keywords = get_keywords() # get_keywords() : 빅토리아가 구축해놓은 Keywords RDBMS에서 Keywords를 전부 가져오는 함수 -> 빅이 RDBMS만 구축해주면 됨
    response = keywords_filtering_model.get_response_by_json(company=company, keywords=keywords) # response : 주어진 기업과 관련있는 Keywords만 필터링된 결과 (형식 : {"keywords": ["키워드1", "키워드2", ...]})
    return response
  
#@app.get("/news/ids/company/{company}/keywords/{keywords}")
#async def get_news_ids_about_company(company: str, keywords: str):
#     pass
  
@app.get("/news/summary/company/{company}/news/{news_ids}")
async def get_keywords_about_company(company: str, news_ids: str):
    # # news = get_news(news_ids) # get_news(news_ids) : 빅토리아가 구축해놓은 News RDBMS에서 News를 전부 가져오는 함수 -> 이것 또한 빅이 RDBMS만 구축해주면 됨
    response = summary_model.get_response_by_json(company=company, news=news)
    return response

# if __name__ == "__main__":
#     response = keywords_filtering_model.get_response_by_json(company="삼성전자", keywords=keywords)
#     print(response["keywords"])
#     # response = summary_model.get_response_by_json(company="삼성전자", news=news)
#     # print(response)

# 기업정보 가져오기
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from finance.stock_api import get_stock_info
from config.db_config import MySQLSelector

@app.get("/api/stock-info/{company_id}")
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