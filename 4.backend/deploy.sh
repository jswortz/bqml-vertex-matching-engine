#!/bin/bash

source ../0.setup/env_vars.sh

PROJECT_NUMBER=$(gcloud projects describe "${RECAI_PROJECT}" | grep projectNumber | cut -d\' -f2)
export PROJECT_NUMBER

CLOUD_SQL_IP=$(gcloud sql instances describe pso-css-retail | grep -i ipAddress: | cut -d: -f2 | cut -d" " -f2)
export CLOUD_SQL_IP

gcloud app deploy --project="${RECAI_PROJECT}"
