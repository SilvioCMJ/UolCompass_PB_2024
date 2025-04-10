FROM python:3.12

WORKDIR /app

COPY requirements.txt /app

RUN pip install --no-cache-dir --upgrade pip 

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 3000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000"]