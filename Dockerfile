# 1. 베이스 이미지: 가볍고 빠른 파이썬 3.9 슬림 버전을 가져옵니다.
FROM python:3.9-slim

# 2. 작업 공간: 컨테이너 안에서 우리가 작업할 폴더를 만듭니다.
WORKDIR /app

# 3. 환경 세팅: requirements.txt를 복사하고 colorama를 설치합니다.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. 소스 코드 복사: 우리의 핵심인 scanner.py 코드를 컨테이너 안으로 가져옵니다.
COPY scanner.py .

# 나중에 이렇게 바꾸면 완벽한 CLI 툴이 됩니다!
ENTRYPOINT ["python", "scanner.py"]
