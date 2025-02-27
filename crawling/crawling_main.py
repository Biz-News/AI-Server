# 진짜 죄송해요 거지같은 코드로 가겠습니다 ㅜㅜㅜㅜㅜㅜㅜㅜㅜ
# 클래스 따윈 없어요 ㅜㅜㅜㅜㅜㅜㅜㅜㅜㅜ
# 검색마다 10페이지 긁어 오는데 시간 완젼 많이 걸려요.... 머리 팡팡 터집니다~!


import requests
from bs4 import BeautifulSoup
from datetime import datetime
import mysql.connector
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


## 거지 함수 쇼
def load_url(url) :
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.content, 'html.parser')
    else:
        print('error')

def AJnews(company, company_id) :
    global ajnum, ajtitle_list, keyword_set
    data_list = []
    for page in range(1, 11):

        # 이동 페이지 설정
        url = f'https://www.ajunews.com/search?page={page}&sdate=2024.02.02&edate=2025.02.26&q={company}&dateview=4&ds=&writer=&writerId=&search_gubun=A'
        soup = load_url(url)

        # 기사 리스트 로드
        news_list = soup.find('ul', attrs={'class': 'news_list'})
        hrefs = [a['href'] for a in news_list.find_all('a', href=True)]

        for news in hrefs:
            # 기사ㅏ id : 아주경제 20 + 6자리 순서 지정
            news_id = 'aj' + str(ajnum).zfill(6)

            # 기사 이동(기사 URL)
            news_url = news
            soup_sub = load_url(news_url)
            # print(news_url)

            # 키워드
            keyword_box = soup_sub.find('ul', attrs={'class': 'keyword_box'})
            if keyword_box:
                keyword = [a.get_text()[1:] for a in keyword_box.find_all('a')]
                if company not in keyword:
                    keyword.append(company)
                # print(keyword)
            else:
                # 키워드가 없으면 다음으로 넘어감
                continue
            keyword_set += keyword

            # 기사 제목
            try:
                title = soup_sub.find('div', class_='inner font_num1').find('h1').get_text(strip=True)
            except AttributeError:
                title = soup_sub.find('div', class_='inner font_num2').find('h1').get_text(strip=True)
            finally:
                # print(title)
                pass
            if title in ajtitle_list:
                continue
            else:
                ajtitle_list.append(title)

            # 날짜
            date = soup_sub.find('dl', class_='flex info').find('dd', class_='date').find('span').get_text(
                strip=True)
            date = datetime.strptime(date, "%Y-%m-%d %H:%M")
            # print(date)

            # 기사 소제목
            try:
                sub_title = '\n'.join(
                    [a.get_text() for a in soup_sub.find('ul', class_='sub_title').find_all('li')])
            except AttributeError:
                sub_title = ''
            finally:
                # print(sub_title)
                pass

            # 기사 본문
            article = soup_sub.find('div', class_='article_con', id='articleBody')
            byline = article.find('div', class_='byline flex')  # 기자 정보 삭제
            if byline:
                byline.decompose()
            for tag in article.find_all(['figure', 'figcaption', 'script', 'ul', 'p']):  # 기타 사진 삭제
                tag.decompose()
            article_text = article.get_text(separator='\n', strip=True)
            # print(article_text)

            data = {'company': company, 'company_id': company_id, 'news_id': news_id, 'url': news_url,
                    'keyword': keyword, 'title': title, 'date': date, 'sub_title': sub_title,
                    'article_text': article_text}

            data_list.append(data)

            # num 업데이트
            ajnum += 1

    return data_list

def ETnews(company, company_id) :
    global etnum, ettitle_list, keyword_set
    data_list = []
    for page in range(1, 11):

        url = f'https://www.etoday.co.kr/search/?keyword={company}&fldTermStart=&fldTermEnd=&fldTermType=1&fldSort=1&page={page}'

        soup = load_url(url)

        # 기사 리스트 로드
        news_list = soup.find_all('li', attrs={'class': 'sp_newslist'})
        hrefs = [a.find('a')['href'] for a in news_list]

        for news in hrefs:
            # 기사ㅏ id : 이투데이 30 + 6자리 순서 지정
            news_id = '30' + str(etnum).zfill(6)

            # 기사 이동(기사 URL)
            news_url = 'https://www.etoday.co.kr/' + news
            soup_sub = load_url('https://www.etoday.co.kr/' + news)
            # print(news_url)

            # 키워드
            keyword_box = soup_sub.find('div', class_='kwd_tags')
            if keyword_box:
                keyword = [a.get_text()[1:] for a in keyword_box.find_all('a')]
                if company not in keyword:
                    keyword.append(company)
                # print(keyword)
            else:
                # 키워드가 없으면 다음으로 넘어감
                continue
            keyword_set += keyword


            # 기사 제목
            title = soup_sub.find('h1', class_='main_title').get_text(strip=True)
            if title in ettitle_list:
                continue
            else:
                ettitle_list.append(title)
            # print(title)

            # 날짜
            date = soup_sub.find('div', class_='newsinfo').find('p').get_text(strip=True)[3:]
            date = datetime.strptime(date, "%Y-%m-%d %H:%M")

            # 기사 소제목
            try:
                sub_title = '\n'.join([a.get_text(strip=True) for a in soup_sub.find_all('sapan', class_='stitle')])
            except AttributeError:
                sub_title = ''
            finally:
                # print(sub_title)
                pass

            # 기사 본문
            article_div = soup_sub.find("div", class_="articleView")
            article_text = "\n".join(
                p.get_text(strip=True) for p in article_div.find_all("p") if p.get_text(strip=True))
            # print(article_text)

            etnum += 1

            data = {'company': company, 'company_id': company_id, 'news_id': news_id, 'url': news_url,
                    'keyword': keyword, 'title': title, 'date': date, 'sub_title': sub_title,
                    'article_text': article_text}

            data_list.append(data)

    return data_list

def Jnews(company, company_id) :
    global jnum, jtitle_list, keyword_set
    data_list = []

    for page in range(1, 11):
        # 이동 페이지 설정
        url = f'https://www.joongang.co.kr/search/news?keyword=={company}&page={page}'
        soup = load_url(url)

        # 기사 리스트 로드
        news_list = soup.find_all('li', class_='card')
        hrefs = []
        for a in news_list:
            link_tag = a.find("a", href=True)
            if link_tag:
                hrefs.append(link_tag["href"])

        for news in hrefs:
            # 기사 id : 중앙일보 40 + 6자리 순서 지정
            news_id = '40' + str(jnum).zfill(6)

            # 기사 이동(기사 URL)
            news_url = news
            soup_sub = load_url(news_url)
            # print(news_url)

            # 키워드
            keyword_box = soup_sub.find('div', class_='tag_wrap')
            if keyword_box:
                keyword = [a.get_text()[2:] for a in keyword_box.find_all('a', class_='tag')]
                if company not in keyword:
                    keyword.append(company)
            else:
                continue
            keyword_set += keyword
            # print(keyword)

            # 기사 제목
            title = soup_sub.find('h1', class_='headline').get_text(strip=True)
            if title in jtitle_list:
                continue
            else:
                jtitle_list.append(title)
            # print(title)

            # 날짜
            try:
                date = soup_sub.find('time', {'itemprop': 'dateModified'})['datetime']
            except AttributeError:
                try:
                    date = soup_sub.find('time', {'itemprop': 'datePublished'})['datetime']
                except AttributeError:
                    continue
            except :
                continue
            finally:
                try :
                    date = datetime.fromisoformat(str(date)).replace(tzinfo=None).strftime("%Y-%m-%d %H:%M:%S")
                except UnboundLocalError :
                    continue

            # 기사 소제목 : 여긴 없음
            sub_title = ''

            # 기사 본문
            article_body = soup_sub.find("div", {"id": "article_body"})
            article_text = "\n".join([p.get_text(strip=True) for p in article_body.find_all("p")[:-1]])
            # print(article_text)

            jnum += 1

            data = {'company': company, 'company_id': company_id, 'news_id': news_id, 'url': news_url,
                    'keyword': keyword, 'title': title, 'date': date, 'sub_title': sub_title,
                    'article_text': article_text}


            data_list.append(data)
    return data_list

# 기업 이름 리스트
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

ajnum = 1
etnum = 1
jnum = 1
ajtitle_list = []
ettitle_list = []
jtitle_list = []
keyword_set = []

# 크롤링 메인
for company in company_list:
    cursor.execute("SELECT company_id FROM company WHERE company = %s", (company,))
    company_data = cursor.fetchone()

    # 아이디 할당
    company_id = company_data[0]

    # 데이터 저장
    data_list = []

    ## 아주경제
    data_list += AJnews(company, company_id)

    ## 이투데이
    data_list += ETnews(company, company_id)

    ## 중앙일보
    data_list += Jnews(company, company_id)


print("크롤링 끝")

# 키워드 id 생성
keyword_set = set(keyword_set)
keyword_set = sorted(list(keyword_set))
keyword_id_set = []

# 본격 디비 저장
for k_idx, keyword in enumerate(keyword_set):
    # 키워드 아이디 생성
    keyword_id = 'k' + str(k_idx).zfill(6)
    keyword_id_set.append(keyword_id)

    # 키워드 테이블 삽입
    insert_query = """INSERT INTO keyword (keyword_id, keyword)
                      VALUES (%s, %s)"""
    query_data = (keyword_id, keyword)
    cursor.execute(insert_query, query_data)

# 뉴스 관련 삽입
for news in data_list :
    news_id = news['news_id']
    url = news['url']
    title = news['title']
    sub_title = news['sub_title']
    article_text = news['article_text']

    if isinstance(news['date'], str):
        date = datetime.strptime(news['date'], "%Y-%m-%d %H:%M:%S")
    else:
        date = news['date']

    # 뉴스 테이블 삽입
    insert_query = """INSERT INTO news (news_id, url, title, sub_title, article_text, date)
                      VALUES (%s, %s, %s, %s, %s, %s)"""
    query_data = (news_id, url, title, sub_title, article_text, date)
    cursor.execute(insert_query, query_data)

    # 뉴스 키워드 관계 테이블
    for i in news['keyword'] :
        keyword_id = keyword_id_set[keyword_set.index(i)]

        # 키워드 뉴스 관계 테이블 삽입
        insert_query = """INSERT INTO news_keyword (keyword_id, news_id)
                              VALUES (%s, %s)"""
        query_data = (keyword_id, news_id)
        cursor.execute(insert_query, query_data)


# 변경 사항 커밋
cnx.commit()

# 연결 종료
cursor.close()
cnx.close()



