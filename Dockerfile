# FROM python:3

# ENV PYTHONUNBUFFERED 1

# WORKDIR /code

# COPY requirements.txt /code/

# RUN pip install -r requirements.txt

# COPY . /code/

# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entrypoint script into the container
COPY entrypoint.sh /entrypoint.sh

# Make entrypoint.sh executable
RUN chmod +x /entrypoint.sh

# Run entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]