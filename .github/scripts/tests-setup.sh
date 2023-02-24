#!/bin/sh
# This scripts sets up the environment for the tests to run.

set -e
# Install the spacy models that are used in the tests.
python -m spacy download en_core_web_sm