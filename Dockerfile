# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Set environment variable for the database URL
ENV DATABASE_URL=postgresql+asyncpg://fastapi_user:123456@db:5432/fastapi_db

# Install system dependencies for PostgreSQL and other essential tools
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies without caching for a smaller image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI application code
COPY ./app ./app
COPY ./db ./db

# Expose port 8000 to allow external traffic to the container
EXPOSE 8000

# Command to run the application using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
