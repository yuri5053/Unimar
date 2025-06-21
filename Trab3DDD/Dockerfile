FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
COPY test_structure.py .
RUN mkdir -p src/database
EXPOSE 5001
ENV FLASK_APP=src/main.py
ENV FLASK_ENV=production
ENV PYTHONPATH=/app
CMD ["python", "src/main.py"]