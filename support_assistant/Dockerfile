FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir --only-binary=:all: -r requirements.txt

COPY . /app/support_assistant

ENV PYTHONPATH=/app
ENV MOCK_LLM=1

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "support_assistant.main:app", "--host", "0.0.0.0", "--port", "8000"]