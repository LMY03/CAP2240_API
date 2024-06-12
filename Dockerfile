FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/

RUN apt-get update && apt-get install -y

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . /app/

# COPY CAP2240_API/inventory/hosts /inventory/hosts

#############################################################

# # Use an official Python runtime as a parent image
# FROM python:3.8-slim-buster

# # Set the working directory in the container
# WORKDIR /code

# # Copy the current directory contents into the container at /code
# COPY . /code

# # Install any needed packages specified in requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the entrypoint script
# COPY entrypoint.sh /code/entrypoint.sh

# # Make port 5000 available to the world outside this container
# EXPOSE 5000

# # Set the entrypoint script
# ENTRYPOINT ["/code/entrypoint.sh"]

# # Run the Django server
# CMD ["python", "manage.py", "runserver", "0.0.0.0:5000"]
