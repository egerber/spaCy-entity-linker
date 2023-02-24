#!/bin/sh
set -e

echo "Running tests..."
python -m unittest discover tests
echo "Tests passed!"