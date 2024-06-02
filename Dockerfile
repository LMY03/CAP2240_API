# FROM python:3

# ENV PYTHONUNBUFFERED 1

# WORKDIR /app

# COPY requirements.txt /app/

# RUN pip install -r requirements.txt

# RUN apt-get update && apt-get install -y

# COPY . /app/

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

#############################################################

# Use the official Python image from the Docker Hub
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y

# Copy the rest of the application code
COPY . /app/

# Copy the entrypoint.sh script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# The command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
