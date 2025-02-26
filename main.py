from fastapi import FastAPI

app = FastAPI()

from app.model import SingleResponseModel
from app.DB import DB
from app.raw import keywords_filtering_prompt_text, summary_prompt_text

from test.test_news import news
from test.test_keywords import keywords

keywords_filtering_model = SingleResponseModel(keywords_filtering_prompt_text)
summary_model = SingleResponseModel(summary_prompt_text)

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
    # news = get_news(news_ids) # get_news(news_ids) : 빅토리아가 구축해놓은 News RDBMS에서 News를 전부 가져오는 함수 -> 이것 또한 빅이 RDBMS만 구축해주면 됨
    response = summary_model.get_response_by_json(company=company, news=news)
    return response

@app.get("/company/{company}")
async def for_front(company: str):
    
  
# if __name__ == "__main__":
#     response = keywords_filtering_model.get_response_by_json(company="삼성전자", keywords=keywords)
#     print(response["keywords"])
#     # response = summary_model.get_response_by_json(company="삼성전자", news=news)
#     # print(response)