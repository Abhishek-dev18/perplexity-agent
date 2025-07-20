FROM mcr.microsoft.com/playwright/python:v1.53.0-jammy

WORKDIR /code
COPY app/ /code/app
RUN pip install --no-cache-dir -r /code/app/requirements.txt \
    && playwright install --with-deps chromium

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]

