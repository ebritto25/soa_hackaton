# Imagem do Python
FROM python:3.10-slim

# Diretório de trabalho
WORKDIR /app

# Arquivo de dependências
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia tudo (.json, .h5, etc)
COPY . .

# Porta utilizada
EXPOSE 7860

# Inicia a API na porta definida
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]