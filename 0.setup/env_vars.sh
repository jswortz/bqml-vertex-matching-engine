#!/bin/bash

# Your account in cloud
export MY_ACCOUNT="babrams@google.com"

# Base project variables
export RECAI_PROJECT="babrams-recai-demo"
export PRIMARY_LOCATION="us-central"
export PRIMARY_REGION="us-central1"
export PRIMARY_ZONE="us-central1-c"
export SECONDARY_LOCATION="us-west1"
export SECONDARY_REGION="us-west1"
export SECONDARY_ZONE="us-west1-a"

# Recommendations AI variables
export RECAI_SA="recai-predict-sa"
export HP_PLACEMENT="homepage"  # homepage placement id
export FBT_PLACEMENT="copurchased"  # frequently bought together placement id
export OYML_PLACEMENT="pdp"  # others you may like placement id
export RVD_PLACEMENT="recently_viewed_default"

gcloud config set project "${RECAI_PROJECT}"

# Creating Terraform variables sourced from above where possible
export TF_VAR_project="${RECAI_PROJECT}"
export TF_VAR_myaccount="${MY_ACCOUNT}"
export TF_VAR_location="${PRIMARY_LOCATION}"
export TF_VAR_region="${PRIMARY_REGION}"
export TF_VAR_zone="${PRIMARY_ZONE}"
export TF_VAR_beta_location="${SECONDARY_LOCATION}"
export TF_VAR_beta_region="${SECONDARY_REGION}"
export TF_VAR_beta_zone="${SECONDARY_ZONE}"

# Custom BQML variables
export BQML_NAME="mf_test"
