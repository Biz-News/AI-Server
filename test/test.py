from model import SingleResponseModel
from raw import keywords_filtering_prompt_text, summary_prompt_text

from test_news import news
from test_keywords import keywords
from test_companies import companies

if __name__ == "__main__":
    keywords_filtering_model = SingleResponseModel(keywords_filtering_prompt_text)
    summary_model = SingleResponseModel(summary_prompt_text)
    response = keywords_filtering_model.get_response_by_json(company=companies[1], keywords=keywords)
    print(response["keywords"])
    # response = summary_model.get_response_by_json(company="삼성전자", news=news)
    # print(response)