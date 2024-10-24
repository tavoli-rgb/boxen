FROM python:3.8-slim

WORKDIR /code

# Install git
RUN apt-get update && apt-get install -y git && apt-get clean

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]