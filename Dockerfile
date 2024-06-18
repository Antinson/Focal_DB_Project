FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5004

<<<<<<< Updated upstream
CMD ["python", "app.py"]
=======
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
>>>>>>> Stashed changes
