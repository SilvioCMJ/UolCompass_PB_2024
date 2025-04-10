# Use uma imagem base com Python
FROM python:3.11-slim

# Defina o diretório de trabalho no container
WORKDIR /app

# Instale dependências do sistema
RUN apt-get update && apt-get install -y gcc libpq-dev && apt-get clean

# Copie os arquivos de requisitos para o container e instale as dependências
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copie todo o código do projeto para o container
COPY . /app/

# Crie um usuário não root para executar o aplicativo (opcional, mas recomendado)
RUN useradd -m appuser
USER appuser

# Exponha a porta 80
EXPOSE 80

# Comando para rodar o Gunicorn no container
CMD ["gunicorn", "--bind", "0.0.0.0:80", "app.wsgi:application"]
