#!/bin/sh

# Define a temporary directory
TEMP_DIR=$(mktemp -d)

# Clone the latest code from the repository into the temporary directory
git clone -b $REPO_BRANCH $REPO_URL $TEMP_DIR

# Copy the relevant files to the /code directory
cp -r $TEMP_DIR/app.py $TEMP_DIR/templates /code/

# Clean up the temporary directory
rm -rf $TEMP_DIR

# Start the Flask app
exec flask run --host=0.0.0.0 --port=5000