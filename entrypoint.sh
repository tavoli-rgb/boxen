#!/bin/sh
# Exit immediately if a command exits with a non-zero status
set -e

# Set default branch to main if not provided
REPO_BRANCH=${REPO_BRANCH:-main}

# Clone or pull the repository
if [ ! -d web/.git ]; then
    # Leeren Sie das web-Verzeichnis, bevor Sie das Repository klonen
    find web -mindepth 1 -delete
    git clone -b ${REPO_BRANCH} --single-branch ${REPO_URL} web
else
    git -C web pull origin ${REPO_BRANCH}
fi

# Start the Flask application
exec "$@"