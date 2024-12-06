#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status.

TEMP_DIR=$(mktemp -d -p .)
TARGET_DIR=./src/jaqpot_api_client

# Install openapi-generator-cli if not already installed
if ! command -v openapi-generator-cli &> /dev/null
then
    echo "openapi-generator could not be found, installing..."
    npm install @openapitools/openapi-generator-cli -g
fi

# Generate the OpenAPI client in a temporary directory
openapi-generator-cli generate \
    -i https://raw.githubusercontent.com/ntua-unit-of-control-and-informatics/jaqpot-api/refs/heads/main/src/main/resources/openapi.yaml \
    -g python \
    -o $TEMP_DIR \
    --additional-properties packageName=jaqpot_api_client

# Ensure the target directory exists
mkdir -p $TARGET_DIR

# Move only the necessary files
cp -r $TEMP_DIR/jaqpot_api_client/* $TARGET_DIR/

# Clean up
rm -rf $TEMP_DIR

echo "OpenAPI client generated successfully in $TARGET_DIR"
