# 1️⃣ 베이스 이미지 (Python 3.11 사용)
FROM python:3.11

# 2️⃣ 작업 디렉토리 설정
WORKDIR /app

# 3️⃣ 필요한 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4️⃣ 환경 변수 설정 (환경 변수 자동 로드)
ENV GOOGLE_API_KEY=${GOOGLE_API_KEY}
ENV OPENAI_API_KEY=${OPENAI_API_KEY}
ENV GOOGLE_API_KEY=${GOOGLE_API_KEY}
ENV OPENAI_API_KEY=${OPENAI_API_KEY}
ENV DB_USER=${DB_USER}
ENV DB_PASSWORD=${DB_PASSWORD}
ENV DB_HOST=${DB_HOST}
ENV DB_PORT=${DB_PORT}
ENV DB_NAME=${DB_NAME}

# 5️⃣ 소스 코드 복사
COPY . .

# 6️⃣ FastAPI 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
