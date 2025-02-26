from dataclasses import dataclass
from datetime import datetime

@dataclass
class News:
  news_id: int
  # url: str
  title: str
  sub_title: str
  content: str
  # date: datetime

  def __str__(self):
    return f"""
  ## 뉴스 ID : {self.news_id}
  제목 : {self.title}
  소제목 : {self.sub_title}
  내용 : {self.content}
  """
  