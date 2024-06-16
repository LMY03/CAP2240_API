RUN rm -rf /app/ansible/artifacts

FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/

RUN apt-get update && apt-get install -y

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . /app/

RUN chmod +x /app/ansible/inventory/dynamic_inventory.py

# COPY CAP2240_API/inventory/hosts /inventory/hosts