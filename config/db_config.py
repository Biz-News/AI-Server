import os
import mysql.connector
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 환경 변수에서 DB 정보 가져오기
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
port = os.getenv("DB_PORT", "3306")
name = os.getenv("DB_NAME")
host = os.getenv("DB_HOST")

# DB 설정 정보
db_config = {
    "host": host,
    "user": user,
    "password": password,
    "database": name,
    "port": int(port)
}

def get_connection():
    """
    DB 연결을 반환하는 함수
    """
    return mysql.connector.connect(**db_config)

class MySQLSelector:
    @staticmethod
    def get_company_info(company_id):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        
        try:
            cursor.execute(
                "SELECT company_id, company_name, ticker FROM companies WHERE company_id = %s",
                (company_id,)
            )
            result = cursor.fetchone()
            
            if not result:
                return None
                
            return result
        except Exception as e:
            print(f"데이터베이스 오류: {str(e)}")
            return None
        finally:
            cursor.close()
            connection.close()