#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

# Set default branch to main if not provided
REPO_BRANCH=${REPO_BRANCH:-main}

# Clone or pull the repository
if [ ! -d .git ]; then
    git clone -b ${REPO_BRANCH} ${REPO_URL} .
else
    git -C . pull origin ${REPO_BRANCH}
fi

# Start the Flask application
exec "$@"