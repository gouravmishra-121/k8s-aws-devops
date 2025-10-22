FROM python:3.10-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .


# Use gunicorn for production-like server
CMD ["gunicorn", "app:app", "-w", "4", "-b", "0.0.0.0:5000"]