import os
import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv

load_dotenv()

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
port = os.getenv("DB_PORT")
name = os.getenv("DB_NAME")
host = os.getenv("DB_HOST")

# AWS RDS 정보
db_config = {
    "host": host,  # AWS RDS 엔드포인트
    "user": user,
    "password": password,
    "database": name,
}

try:
  cnx = mysql.connector.connect(**db_config)
  cursor = cnx.cursor()
  cursor.execute("USE {}".format(name))
  cursor.execute("SELECT * FROM company")
  all = cursor.fetchall()
  for a in all:
      print(a)
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
  cnx.close()

# # MySQL 연결
# conn = mysql.connector.connect(**db_config)
# cursor = conn.cursor()

# # 데이터 조회
# cursor.execute("SELECT * FROM your_table")
# rows = cursor.fetchall()

# for row in rows:
#     print(row)

# # 연결 닫기
# cursor.close()
# conn.close()