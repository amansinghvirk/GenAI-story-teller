#!/bin/bash

# Script to deploy a Flask application to Google Cloud Run, leveraging Vertex AI and Secret Manager.

# --- Environment Variables ---
# Set environment variables for the project, region, service accounts, and application specifics.
export PROJECT_ID=gcp-project-name                           # Google Cloud Project ID.
export REGION="us-central1"                                 # Google Cloud Region to deploy resources in.
export SVC_ACCOUNT=service-account                      # Service account name for the application.
export REPO="story-teller-sp-repo"                           # Artifact Registry repository name for docker images.
export SECRET_ID="STORY_TELLER_APP"                         # Secret Manager secret ID to store service account credentials.
export APP_NAME="story-teller"                              # Name of the Cloud Run application.
export APP_VERSION="0.1"                                    # Version of the application being deployed.

# --- Google Cloud Configuration ---
# Set the current Google Cloud project.
gcloud config set project $PROJECT_ID

# Delete the service account
export SVC_ACCOUNT_EMAIL=$SVC_ACCOUNT@$PROJECT_ID.iam.gserviceaccount.com
gcloud iam service-accounts delete $SVC_ACCOUNT_EMAIL  --quiet

# Delete the artifacts registry
gcloud artifacts repositories delete $REPO \
    --location=$REGION \
     --quiet

# Delete secret manager to store credentials
gcloud secrets delete $SECRET_ID --quiet

# Delete deployed Cloud Run App
gcloud run services delete $APP_NAME --region=$REGION --quiet