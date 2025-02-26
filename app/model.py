from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv
import json
import re

class SingleResponseModel:
  def __init__(self, prompt_text):
    # .env 파일 로드 (로컬 환경에서만)
    if os.getenv("CI") is None:  # CI/CD 환경이 아니면 .env 로드
        load_dotenv()
    self.model = ChatGoogleGenerativeAI(
        model='gemini-1.5-pro',
        max_tokens=None,
        timeout=None,
        max_retries=3,
    )
    model = init_chat_model("gpt-4o", model_provider="openai")
    self.prompt_template = PromptTemplate.from_template(prompt_text)
  def get_prompt(self, **kwargs):
    return self.prompt_template.invoke(kwargs)
  def invoke(self, **kwargs):
    prompt = self.get_prompt(**kwargs)
    return self.model.invoke(prompt)
  def get_response_by_json(self, **kwargs):
    response = self.invoke(**kwargs)
    cleaned_content = re.sub(r"^```json\n|\n```$", "", response.content, flags=re.MULTILINE)
    jsoned_content = json.loads(cleaned_content)
    return jsoned_content