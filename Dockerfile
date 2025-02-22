FROM python:3.12.1-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py \
    FLASK_ENV=production

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the application code
COPY . .

# Run the application with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "my_app:create_app"]

