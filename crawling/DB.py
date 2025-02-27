import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
port = os.getenv("DB_PORT")
name = os.getenv("DB_NAME")
host = os.getenv("DB_HOST")

#AWS RDS 정보
db_config = {
    "host": host,  # AWS RDS 엔드포인트
    "user": user,
    "password": password,
    "database": name,
}
cnx = mysql.connector.connect(**db_config)
cursor = cnx.cursor()

#DB 확인
cursor.execute(f'USE {name};')

# news 뉴스 table
cursor.execute('''
CREATE TABLE IF NOT EXISTS news (
    news_id VARCHAR(36) PRIMARY KEY,
    url VARCHAR(255),
    title VARCHAR(255),
    sub_title TEXT,                 # 크기에 따라 조절 MEDIUMTEXT, LONGTEXT
    article_text TEXT,
    date DATETIME
)
''')

# keyword 키워드 table
cursor.execute('''
CREATE TABLE IF NOT EXISTS keyword (
    keyword_id VARCHAR(36) PRIMARY KEY,
    keyword VARCHAR(255)
)
''')

# news_keyword 뉴스 키워드 관계
cursor.execute('''
CREATE TABLE IF NOT EXISTS news_keyword (
    keyword_id VARCHAR(36),
    news_id VARCHAR(36),
    PRIMARY KEY (keyword_id, news_id),
    FOREIGN KEY (keyword_id) REFERENCES keyword(keyword_id) ON DELETE CASCADE,
    FOREIGN KEY (news_id) REFERENCES news(news_id) ON DELETE CASCADE

)
''')



# company 기업
cursor.execute('''
CREATE TABLE IF NOT EXISTS company (
    company_id VARCHAR(36) PRIMARY KEY,
    company VARCHAR(255)
)
''')

# company_keyword 기업 키워드 관계
cursor.execute('''
CREATE TABLE IF NOT EXISTS company_keyword (
    keyword_id VARCHAR(36),
    company_id VARCHAR(36),
    PRIMARY KEY (keyword_id, company_id),
    FOREIGN KEY (keyword_id) REFERENCES keyword(keyword_id) ON DELETE CASCADE,
    FOREIGN KEY (company_id) REFERENCES company(company_id) ON DELETE CASCADE

)
''')


company_list = [
    "삼성전자",
    "현대자동차",
    "기아",
    "LG전자",
    "SK하이닉스",
    "네이버",
    "카카오",
    "삼성생명",
    "삼성물산",
    "현대모비스",
    "SK이노베이션",
    "LG화학",
    "포스코홀딩스",
    "한화솔루션",
    "대한항공",
    "아시아나항공",
    "CJ제일제당",
    "롯데쇼핑",
    "삼성SDI",
    "셀트리온",
    "삼성바이오로직스",
    "엔씨소프트",
    "넷마블",
    "하이브",
    "현대건설",
    "두산에너빌리티",
    "에코프로",
    "한국전력공사",
    "LG에너지솔루션",
    "KB금융"
]


for idx, company in enumerate(company_list, start=1):
    company_id = 'c'+ str(idx).zfill(6)
    cursor.execute('''
                        INSERT INTO company (company_id, company)
                        VALUES (%s, %s)
                    ''', (company_id, company) )


cursor.execute("show tables")
result = cursor.fetchall()
for row in result:
    print(row)


# 변경 사항 커밋
cnx.commit()

# 연결 종료
cursor.close()
cnx.close()