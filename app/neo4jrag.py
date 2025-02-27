import asyncio

from DB import DB

from langchain.chat_models import init_chat_model
from langchain_neo4j import GraphCypherQAChain, Neo4jGraph
from langchain.prompts import PromptTemplate

class Neo4jRAG:
    def __init__(self):
        self.graph = Neo4jGraph(
            url = "bolt://13.124.216.60:7687/",
            username = "neo4j", 
            password = "123456789",
        )
        self.model = init_chat_model("gpt-4o", model_provider="openai", temperature=0)

    async def get_related_nodes(self, company, node, top_k=7):
        cypher_chain = GraphCypherQAChain.from_llm(self.model, self.graph, top_k=top_k)
        prompt_text = "당신은 {company} 기업에 관심이 많은 사람입니다. 그래서 해당 기업에 대한 뉴스를 매일 확인하여 관련된 {node}를 분석하고 있습니다. 최근 {company} 기업과 함께 뉴스에 언급이 많이 된 {node}를 추출해 주세요. 각각의 키워드는 쉼표(,)로 구분되어 있습니다."
        prompt_template = PromptTemplate.from_template(prompt_text)
        prompt = prompt_template.invoke({"company": company, "node": node})
        result = await cypher_chain.ainvoke(prompt)
        return result

    # async def get_related_news_ids(company, keywords, graph):
    #     cypher_chain = GraphCypherQAChain.from_llm(self.model, self.graph, top_k=top_k)
    #     prompt_text = "당신은 {company} 기업에 관심이 많은 사람입니다. 그래서 해당 기업에 대한 뉴스를 매일 확인하여 관련된 {node}를 분석하고 있습니다. 최근 {company} 기업과 함께 뉴스에 언급이 많이 된 {node}를 추출해 주세요. 각각의 키워드는 쉼표(,)로 구분되어 있습니다."
    #     prompt_template = PromptTemplate.from_template(prompt_text)
    #     prompt = prompt_template.invoke({"company": company, "node": node})
    #     result = await cypher_chain.ainvoke(prompt)
    #     return result

    async def get_news_by_ids_from_MySQL(self, news_ids: list, DB):
        db = DB()
        news = db.get_news_by_ids(news_ids)
        return news

    async def get_news_sentiments(company, news, model):
        prompt_text = "당신은 {company} 기업에 관심이 많은 사람입니다. 그래서 해당 기업에 대한 뉴스를 매일 확인하여 관련된 {node}를 분석하고 있습니다. 최근 {company} 기업과 함께 뉴스에 언급이 많이 된 {node}를 추출해 주세요. 각각의 키워드는 쉼표(,)로 구분되어 있습니다."
        prompt_template = PromptTemplate.from_template(prompt_text)
        prompt = prompt_template.invoke({"company": company, "node": node})
        result = await cypher_chain.ainvoke(prompt)

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
    print(rag)