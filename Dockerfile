# FROM python:3

# ENV PYTHONUNBUFFERED 1

# WORKDIR /app

# COPY requirements.txt /app/

# RUN pip install -r requirements.txt

# COPY . /app/

# Use the official Python image from the Docker Hub
FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN apt-get update
RUN apt-get upgrade
RUN apt-get update && apt-get install -y

# Copy the project files
COPY . .

# Copy the entrypoint script
COPY entrypoint.sh /app/entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# Command to run when the container starts
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]