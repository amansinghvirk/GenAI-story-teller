
#!/bin/bash

# Script to deploy a Flask application to Google Cloud Run, leveraging Vertex AI and Secret Manager.

# --- Environment Variables ---
# Set environment variables for the project, region, service accounts, and application specifics.
export PROJECT_ID=prj-smart-news                            # Google Cloud Project ID.
export REGION="us-central1"                                 # Google Cloud Region to deploy resources in.
export SVC_ACCOUNT="story-teller-sp"                        # Service account name for the application.
export REPO="story-teller-sp-repo"                           # Artifact Registry repository name for docker images.
export SECRET_ID="STORY_TELLER_APP"                         # Secret Manager secret ID to store service account credentials.
export APP_NAME="story-teller"                              # Name of the Cloud Run application.
export APP_VERSION="0.1"                                    # Version of the application being deployed.
export CREDENTIALS_FILE="/secrets/gemini-credentials.json"  # Path of the credentials file within the container.
export LANGUAGE_MODEL="gemini-2.0-flash-exp"                # Language model to be used in the application
export VISION_MODEL="imagegeneration@006"                   # Vision model to be used in the application
export IMAGE_TO_TEXT_MODEL="gemini-1.5-pro"


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
gcloud iam service-accounts keys create /c/mydata/projects/keys/story-teller.json \
  --iam-account=$SVC_ACCOUNT_EMAIL

# Grant the service account the `aiplatform.user` role to access Vertex AI resources
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SVC_ACCOUNT_EMAIL" \
  --role="roles/aiplatform.user"
