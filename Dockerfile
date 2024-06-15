FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/

RUN apt-get update && apt-get install -y

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . /app/

RUN mkdir /ansible/
RUN mkdir /ansible/inventory/
RUN touch /ansible/inventory/hosts
RUN mkdir /ansible/playbooks/
# RUN mv /app/playbooks /ansible/

# COPY CAP2240_API/inventory/hosts /inventory/hosts