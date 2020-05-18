#!/bin/bash

export PROJECT_ID="$(gcloud config get-value project -q)"
docker build -t gcr.io/${PROJECT_ID}/odoo:10.7 .

# export PROJECT_ID="$(gcloud config get-value project -q)"
# docker build --rm -t gcr.io/${PROJECT_ID}/odoo:10.0 .