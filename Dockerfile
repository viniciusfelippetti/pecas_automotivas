# Use a Python base image
FROM python:3.12

WORKDIR /pecas_automotivas

# Set environment variables (optional but good practice)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies (for PostgreSQL and other potential needs)
RUN apt-get update && apt-get install -y wait-for-it \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

CMD ["python", "manage.py", "runserver", "127.0.0.1:8000"]