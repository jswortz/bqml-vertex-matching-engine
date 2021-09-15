#!/bin/bash

source ./env_vars.sh

gcloud services enable \
    iam.googleapis.com \
    cloudresourcemanager.googleapis.com \
    vpcaccess.googleapis.com \
    compute.googleapis.com \
    servicenetworking.googleapis.com \
    appengine.googleapis.com \
    sqladmin.googleapis.com \
    recommendationengine.googleapis.com \
    bigquerydatatransfer.googleapis.com \
    ml.googleapis.com \
    retail.googleapis.com \
    aiplatform.googleapis.com \
    cloudbuild.googleapis.com \
    notebooks.googleapis.com

gcloud iam service-accounts create \
     "${TERRAFORM_SA}"

gcloud projects add-iam-policy-binding \
    "${RECAI_PROJECT}" \
    --member="serviceAccount:${TERRAFORM_SA}@${RECAI_PROJECT}.iam.gserviceaccount.com" \
    --role="roles/owner"

gcloud iam service-accounts keys create \
     ../1.terraform/service_account.json \
     --iam-account "${TERRAFORM_SA}"@"${RECAI_PROJECT}".iam.gserviceaccount.com