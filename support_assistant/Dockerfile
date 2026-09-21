FROM python:3.11-slim

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .

RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir --only-binary=:all: -r requirements.txt

# Copy application
COPY . /app/support_assistant

# Make /app importable as a Python package root
ENV PYTHONPATH=/app

# Required grading mode
ENV MOCK_LLM=1

# Build the ChromaDB knowledge base during image creation
RUN python -m support_assistant.knowledge_base

EXPOSE 8000

# Start FastAPI
CMD ["python", "-m", "uvicorn", "support_assistant.main:app", "--host", "0.0.0.0", "--port", "8000"]