from dataclasses import dataclass
from datetime import datetime


@dataclass
class News:
    news_id: int
    url: str
    title: str
    sub_title: str
    article_text: str
    date: datetime

    def to_json(self):
        return {
            "news_id": self.news_id,
            "url": self.url,
            "title": self.title,
            "sub_title": self.sub_title,
            "article_text": self.article_text,
            "date": self.date
        }
    
    def __str__(self):
        return f"""
  ## 뉴스 ID : {self.news_id}
  제목 : {self.title}
  소제목 : {self.sub_title}
  내용 : {self.article_text}
  """
