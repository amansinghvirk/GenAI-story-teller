source $(pwd)/.env

# Set the current project
gcloud config set project $PROJECT_ID

gcloud services enable \
    aiplatform.googleapis.com \
    generativelanguage.googleapis.com

gcloud iam service-accounts create $SVC_ACCOUNT
export SVC_ACCOUNT_EMAIL=$SVC_ACCOUNT@$PROJECT_ID.iam.gserviceaccount.com
echo $SVC_ACCOUNT_EMAIL

gcloud iam service-accounts keys create $KEY_FILE_PATH \
  --iam-account=$SVC_ACCOUNT_EMAIL

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SVC_ACCOUNT_EMAIL" \
  --role="roles/aiplatform.user"