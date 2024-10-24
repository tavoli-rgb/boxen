FROM python:3.8-slim

WORKDIR /code

# Install git
RUN apt-get update && apt-get install -y git && apt-get clean

# Clone the repository
ARG REPO_URL=https://github.com/tavoli-rgb/boxen.git
RUN if [ ! -d .git ]; then git clone ${REPO_URL} .; else git pull origin main; fi

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]