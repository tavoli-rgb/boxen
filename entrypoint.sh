#!/bin/sh

# Clone or pull the latest code from the repository
if [ ! -d "/code/.git" ]; then
  git clone -b $REPO_BRANCH $REPO_URL /code
else
  cd /code
  git pull origin $REPO_BRANCH
fi

# Start the Flask app
exec flask run --host=0.0.0.0 --port=5000