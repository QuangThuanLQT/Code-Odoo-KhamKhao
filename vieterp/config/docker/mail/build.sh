#!/bin/bash

export PROJECT_ID="$(gcloud config get-value project -q)"
docker build -t gcr.io/${PROJECT_ID}/mail:2.4 .

# docker run -p 1080:1080 -p 1025:1025 -p 25:1025 -d gcr.io/${PROJECT_ID}/mail:2.0