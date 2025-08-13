# 使用輕量版 Python
FROM python:3.10-slim

# 設定工作目錄
WORKDIR /app

# 複製需求檔並安裝
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製全部程式碼
COPY . .

# 設定環境變數
ENV PYTHONUNBUFFERED True
ENV PORT 8080

# 開放 Cloud Run 預設埠
EXPOSE 8080

# 啟動 Flask（port 改成 Cloud Run 預設 8080）
CMD ["python", "app.py"]