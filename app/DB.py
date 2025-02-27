import os
import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv
from app.news import News

# 어떤 query가 필요하나
# 1. keywords 전체
# 2. 뉴스 id 여러개로 한번에


class DB:
    def __init__(self):
        load_dotenv()
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        name = os.getenv("DB_NAME")
        host = os.getenv("DB_HOST")
        db_config = {
            "host": host,
            "user": user,
            "password": password,
            "database": name,
        }
        self.cnx = mysql.connector.connect(**db_config)
        self.cursor = self.cnx.cursor(dictionary=True)
        
    def get_every_keyword(self):
        sql = "SELECT * FROM keyword" # TODO keyword 테이블 이름 바뀌면 수정
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        keywords = [keyword_tuple[0] for keyword_tuple in result]
        return keywords
    
    def get_news_by_ids(self, news_ids: list):
        sql = f"SELECT * FROM news WHERE news_id IN ({', '.join(map(str, news_ids))})" # TODO news 테이블 이름 바뀌면 수정
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        news = [News(*news_tuple) for news_tuple in result] # TODO news가 어떻게 생겼냐에 따라 수정
        return news
    
    def get_company_info(self, company_id):
        sql = "SELECT company_id, company, ticker FROM company WHERE company_id = %s"
        self.cursor.execute(sql, (company_id,))
        return self.cursor.fetchone()
    
    def query(self, sql):
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return [result_tuple for result_tuple in result]

    def close(self):
        self.cursor.close()
        self.cnx.close()
        
# if __name__ == '__main__':
#     db = DB()
#     db.cursor.execute('SELECT * FROM news')
#     print(db.cursor.fetchall())