FROM python:3.12.6-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app.main:app

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
