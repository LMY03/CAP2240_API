FROM python:3

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y

COPY . /app/

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

#############################################################

# # Use the official Python image from the Docker Hub
# FROM python:3.9-slim

# ENV PYTHONUNBUFFERED 1

# # Set the working directory
# WORKDIR /app

# # Copy the requirements file
# COPY requirements.txt /app/

# RUN pip install -r requirements.txt

# # Install the dependencies
# RUN apt-get update && apt-get install -y

# # Copy the project files
# COPY . /app/

# # Make the entrypoint script executable
# RUN chmod +x entrypoint.sh

# # Set the entrypoint
# ENTRYPOINT ["entrypoint.sh"]

# # Command to run when the container starts
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]