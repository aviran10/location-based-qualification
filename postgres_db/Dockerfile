FROM python:3.9-slim

WORKDIR /app

# install requirements
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY ./ /app/

# Copy the data for DB initialization
COPY ./db_data/ /app/db_data/

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Run init_postgres.py on container startup
CMD ["python", "./postgres_db/init_postgres.py"]
