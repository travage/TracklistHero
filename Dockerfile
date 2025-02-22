FROM python:3.12
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
ENV FLASK_APP=app.py
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:create_app()"]

