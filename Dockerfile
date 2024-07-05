FROM python:3.11.5-slim

WORKDIR /focal_db_project

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

ENV PORT 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "wsgi:app"]
