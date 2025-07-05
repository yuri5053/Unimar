# Dockerfile para a API da Biblioteca
# Demonstração de containerização com Docker

FROM python:3.11-slim

# Definir diretório de trabalho
WORKDIR /app

# Copiar arquivo de requirements
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY src/ ./src/
COPY test_structure.py .

# Criar diretório para banco de dados
RUN mkdir -p src/database

# Expor porta da aplicação
EXPOSE 5001

# Definir variáveis de ambiente
ENV FLASK_APP=src/main.py
ENV FLASK_ENV=production
ENV PYTHONPATH=/app

# Comando para iniciar a aplicação
CMD ["python", "src/main.py"]

