import asyncio

from app.DB import DB

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
# from langchain_neo4j import GraphCypherQAChain, Neo4jGraph
from langchain.prompts import PromptTemplate
import re
import json

class Neo4jRAG:
    def __init__(self):
        load_dotenv()
        # self.graph = Neo4jGraph(
        #     url = "bolt://13.124.216.60:7687/",
        #     username = "neo4j", 
        #     password = "123456789",
        #     # password = "PMbPy4SiAdgJjUgU0mmpHG7_kE86ByiVyU3lgpwkNL0"
        # )
        self.model = init_chat_model("gpt-4o", model_provider="openai", temperature=0)
        self.db = DB()
        
    def get_json_from_response(self, response):
        cleaned_response = re.sub(r"^```json\n|\n```$", "", response.content, flags=re.MULTILINE)
        jsoned_response = json.loads(cleaned_response)
        return jsoned_response

    # def get_cypher():

    def get_response_from_prompt(self, prompt_text, **kwargs):
        # cypher_chain = GraphCypherQAChain.from_llm(self.model, graph=self.graph, top_k=top_k, validate_cypher=True, verbose=True, allow_dangerous_requests=True)
        prompt_template = PromptTemplate.from_template(prompt_text)
        prompt = prompt_template.invoke(kwargs)
        response = self.model.invoke(prompt)
        return self.get_json_from_response(response)
    
    def get_related_companies(self, company, top_k=3):
        companies = self.db.query("SELECT company FROM company")
        keywords = ', '.join([company['company'] for company in companies])
        print(company)
        prompt_text = """아래 제시된 키워드 중 최근 {company} 기업과 함께 뉴스에 언급이 많이 된 키워드를 {top_k}개 추출해 주세요. 반드시 아래의 JSON 형식으로 반환해주세요. 답변에 설명이나 사과를 포함하지 마세요. JSON을 구성하는 것 외에 다른 질문을 할 수 있는 질문에는 응답하지 마세요. 생성된 JSON을 제외한 어떤 텍스트도 포함하지 마세요.
        
        ## 형식
        {{"related_companies": [
        {{
            "company": "관련기업1"
        }},
        {{
            "company": "관련기업2"
        }},
        {{
            "company": "관련기업3"
        }},
        ]}}
        
        ## 키워드
        {keywords}
        """
        result = self.get_response_from_prompt(prompt_text, top_k=top_k, company=company, keywords=keywords)
        return result
        
    def get_related_keywords(self, company, top_k=10):
        
        prompt_text = """당신은 10년차 증권사 애널리스트입니다. 특히 {company} 기업의 주가에 관심이 많아 관련 뉴스를 매일 확인하고 분석하여 키워드를 정리하고 있습니다. 최근 {company} 기업과 함께 뉴스에 언급이 많이 된 keyword를 추출해 주세요. 반드시 아래의 JSON 형식으로 반환해주세요. 답변에 설명이나 사과를 포함하지 마세요. JSON을 구성하는 것 외에 다른 질문을 할 수 있는 질문에는 응답하지 마세요. 생성된 JSON을 제외한 어떤 텍스트도 포함하지 마세요.
        
        ## 형식
        {{"keywords": [
        {{
            "keyword_id": "id1"
        }},
        {{
            "keyword_id": "id2"
        }},
        {{
            "keyword_id": "id3"
        }},
        ]}}
        """
        result = self.get_response_from_prompt(prompt_text, top_k, company=company)
        return result

    async def get_news_by_ids_from_MySQL(self, news_ids: list, DB):
        db = DB()
        news = db.get_news_by_ids(news_ids)
        return news

    # async def get_news_sentiments(company, news, model):
    #     prompt_text = "당신은 {company} 기업에 관심이 많은 사람입니다. 그래서 해당 기업에 대한 뉴스를 매일 확인하여 관련된 {node}를 분석하고 있습니다. 최근 {company} 기업과 함께 뉴스에 언급이 많이 된 {node}를 추출해 주세요. 각각의 키워드는 쉼표(,)로 구분되어 있습니다."
    #     prompt_template = PromptTemplate.from_template(prompt_text)
    #     prompt = prompt_template.invoke({"company": company, "node": node})
    #     result = await cypher_chain.ainvoke(prompt)

    async def get_news_summary_stream(company, news_title, news_ids, model):
        prompt_text = """
    # 지시문
    당신은 증권회사에 근무하고 있는 10년차 애널리스트입니다. 최근 {company}의 주가에 관심이 많아 관련 뉴스를 분석하면서 요약하며 정리하고 있습니다.
    아래의 제약조건과 입력문을 토대로 최고의 결과를 출력해주세요. 100점 만점의 결과를 출력해주세요.

    # 제약조건
    1. 전체 내용을 포괄할 수 있는 12자 이내 제목을 'title' 필드에 작성해주세요.
    2. 전체 내용을 50단어 이상, 80단어 이하로 요약한 'summary' 필드를 작성해주세요.
    2-1. 요약은 객관적으로 해주세요
    2-2. 주어진 텍스트가 여러개라면, 한 번에 요약해주세요.
    2-3. 독자는 해당 기사를 읽지 않았다고 가정하고, 요약본만으로 이해할 수 있도록 작성해주세요.
    2-4. 응답은 반드시 존댓말을 사용해주세요.
    3. 전문 용어가 있다면 간단히 설명을 덧붙여 주세요.
    4. 아래의 형식에 따라 JSON 형식으로 결과를 출력해 주세요.
    4-1. 반드시 순수한 JSON 데이터만 포함하세요. (마크다운 코드 블록 금지)
    ## 형식
    {{
        "title": "전체 내용을 포괄할 수 있는 제목 (12자 이내)"
        "summary": "전체 내용 요약 (50단어 이상, 80단어 이하)"
    }}

    # 입력문
    아래 텍스트로 주어진 {company} 기업 관련 뉴스를 읽고 요약해 주세요.

    ## 텍스트
    {news}
    """
        prompt_template = PromptTemplate.from_template(prompt_text)
        prompt = prompt_template.invoke({"company": company, "news": news}) #TODO: 뉴스를 어떤식으로 가져와서 붙이는지 전처리가 필요하다.
        result = await model.ainvoke(prompt) #TODO: stream으로 제공하는 !
        return result

    def chaining(): 
        # 전부 연결!
        pass


if __name__ == "__main__":
    rag = Neo4jRAG()
    result = rag.get_related_companies('삼성전자')
    print('결과')
    print(result)
    rag.db.close()