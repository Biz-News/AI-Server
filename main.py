from fastapi import FastAPI, HTTPException, Path
from finance.stock_api import get_stock_info, format_currency, format_volume
from app.DB import DB
from app.neo4jrag import Neo4jRAG
from dotenv import load_dotenv
from datetime import datetime, timedelta
from pykrx import stock

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
    # 1. MySQL에서 기업 정보 가져오기 (가정)
    company_info = db.get_company_info(company_id)
    if not company_info:
        raise HTTPException(status_code=404, detail="회사 정보를 찾을 수 없습니다.")

    try:
        if "ticker" not in company_info or not company_info["ticker"]:
            raise HTTPException(status_code=404, detail="해당 기업의 종목코드(ticker) 정보가 없습니다.")

        # 2. 주식 정보 조회
        stock_info = get_stock_info(company_info["ticker"])

        # 3. 데이터 변환 적용
        formatted_response = {
            "company_name": company_info.get("company", "정보 없음"),
            "ticker": company_info.get("ticker", "정보 없음"),
            "trading_volume": format_volume(stock_info.get("trading_volume", 0)),
            "trading_value": format_currency(stock_info.get("trading_value", 0)),
            "low_52weeks": format_currency(stock_info.get("low_52weeks", 0)),
            "high_52weeks": format_currency(stock_info.get("high_52weeks", 0)),
            "change_amount": stock_info.get("change_amount", 0),
            "change_percent": stock_info.get("change_percent", 0.0)
        }

        print("Formatted response:", formatted_response)  # FastAPI가 반환하기 전에 확인
        print(type(formatted_response))

        return formatted_response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")
    
@app.get("/companies/stock-info/chart/{days}")
async def get_stock_chart(days: int, ticker: str):
    try:
        # 오늘 날짜 기준으로 시작 날짜 계산
        today = datetime.today()
        start_date = (today - timedelta(days=days)).strftime("%Y%m%d")
        end_date = today.strftime("%Y%m%d")

        # Pykrx를 이용하여 OHLCV 데이터 가져오기
        df = stock.get_market_ohlcv_by_date(start_date, end_date, ticker)

        # DataFrame이 비어있는 경우 예외 처리
        if df.empty:
            raise HTTPException(status_code=404, detail="해당 기간 동안 주식 데이터가 없습니다.")

        # JSON 응답 포맷 변경
        stock_data = [
            {
                "x": date.strftime("%Y-%m-%d"),
                "o": row["시가"],
                "h": row["고가"],
                "l": row["저가"],
                "c": row["종가"]
            }
            for date, row in df.iterrows()
        ]

        return {"stockData": stock_data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")
    
# 연관 기업
@app.get("/companies/{company_id}/related/")
def get_related_companies(company_id: str):
    rag = Neo4jRAG()
    db = DB()
    company = db.query(f'SELECT company FROM company WHERE company_id = "{company_id}"')[0]['company']
    related_companies_name = rag.get_related_companies(company)['related_companies']
    # [{"company":"SK하이닉스"},{"company":"LG전자"},{"company":"삼성SDI"}]
    related_companies = [{'company_id': db.query(f"SELECT company_id FROM company WHERE company = '{company['company']}'")[0]['company_id'], 'company': company['company']} for company in related_companies_name]
    db.close()
    return {'company_id': company_id, "company": company, "related_companies": related_companies}

# 연관 키워드
@app.get("/keywords/{company_id}/related/")
def get_related_companies(company_id: str):
    rag = Neo4jRAG()
    db = DB()
    company = db.query(f'SELECT company FROM company WHERE company_id = "{company_id}"')[0]['company']
    response = rag.get_response_from_prompt("""최근 {company} 기업의 주가에 가장 영향이 있었던 단어 10개를 아래와 같은 형식으로 반환해줘. 그 외의 텍스트 출력은 일절 없어야해. 단어는 띄어쓰기 없는 단어를 말해

#형식
{{
	  "keywords": [
		  {{
			  "keyword_id": "id1",
			  "keyword": "keyword1"
			}},
			{{
			  "keyword_id": "id2",
			  "keyword": "keyword2"
			}},
			{{
			  "keyword_id": "id3",
			  "keyword": "keyword3"
			}},
			...
	  ],
}}""", company=company)
    db.close()
    return response


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
