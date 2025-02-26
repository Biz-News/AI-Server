from fastapi import FastAPI
app = FastAPI()

from model import SingleResponseModel
from raw import keywords_filtering_prompt_text, summary_prompt_text

from test_news import news
from test_keywords import keywords

keywords_filtering_model = SingleResponseModel(keywords_filtering_prompt_text)
summary_model = SingleResponseModel(summary_prompt_text)

@app.get("/company/{company}/keywords")
async def get_keywords_about_company(company: str):
    # keywords = get_keywords()
    response = keywords_filtering_model.get_response_by_json(company=company, keywords=keywords)
    return response
  
@app.get("/news/summary/company/{company}/news/{news_ids}")
async def get_keywords_about_company(company: str, news_ids: str):
    # news = get_news(news_ids)
    response = summary_model.get_response_by_json(company=company, news=news)
    return response
  
# if __name__ == "__main__":
#     response = keywords_filtering_model.get_response_by_json(company="삼성전자", keywords=keywords)
#     print(response["keywords"])
#     # response = summary_model.get_response_by_json(company="삼성전자", news=news)
#     # print(response)