FROM mcr.microsoft.com/playwright/python:v1.53.0-jammy

WORKDIR /code

# Copy application files
COPY app/ /code/app

# Install Python dependencies
RUN pip install --no-cache-dir -r /code/app/requirements.txt \
    && playwright install --with-deps chromium

# Expose port
EXPOSE 8080

# Start the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
