FROM python:3.8-slim

# Install git and MySQL client
RUN apt-get update && apt-get install -y git default-libmysqlclient-dev

WORKDIR /code

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["/code/entrypoint.sh"]