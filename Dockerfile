FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libpq-dev \
    libnss3 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libgbm1 \
    libgtk-3-0 \
    libasound2 \
    libpangocairo-1.0-0 \
    libpango-1.0-0 \
    libxrandr2 \
    libxss1 \
    libxtst6 \
    libappindicator3-1 \
    libatk-bridge2.0-0 \
    libatspi2.0-0 \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN python -m playwright install --with-deps

COPY ./app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
