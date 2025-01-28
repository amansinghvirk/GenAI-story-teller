
#!/bin/bash

# Script to deploy a Flask application to Google Cloud Run, leveraging Vertex AI and Secret Manager.

# --- Environment Variables ---
# Set environment variables for the project, region, service accounts, and application specifics.
export PROJECT_ID="google-project-name"                         # Google Cloud Project ID.
export REGION="us-central1"                                 # Google Cloud Region to deploy resources in.
export SVC_ACCOUNT="service-account-name"                       # Service account name for the application.

# Get the project number.
export PROJECT_NUMBER=$(gcloud projects describe "$PROJECT_ID" --format="value(projectNumber)")

# --- Google Cloud Configuration ---
# Set the current Google Cloud project.
gcloud config set project $PROJECT_ID

# --- Service Account Setup ---
# Create a service account to be used for Vertex AI authorization.
gcloud iam service-accounts create $SVC_ACCOUNT

# Export the service account email for later use.
export SVC_ACCOUNT_EMAIL=$SVC_ACCOUNT@$PROJECT_ID.iam.gserviceaccount.com
echo $SVC_ACCOUNT_EMAIL

# Create and save the service account's JSON credentials key to a local path.
# IMPORTANT: Ensure the path `<local-path-to-save-json-file>` is accessible and secure
gcloud iam service-accounts keys create `<local-path-to-save-json-file>` \
  --iam-account=$SVC_ACCOUNT_EMAIL

# Grant the service account the `aiplatform.user` role to access Vertex AI resources
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SVC_ACCOUNT_EMAIL" \
  --role="roles/aiplatform.user"
