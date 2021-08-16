#!/bin/bash

source ./add_env_vars.sh

# Check if a service has already been deployed, if not deploy default service
existing_service_count=$(gcloud app services list | cut -d" " -f1 | grep -v SERVICE | wc -l)
if [ ${existing_service_count} -lt 1 ]; then
  # Initial deployment with default service name as required by App Engine on clean install
  export APP_ENGINE_SERVICE="default"
  python3 build_app_yaml.py
  gcloud app deploy --project="${RECAI_PROJECT}"
fi

# Actual deployment to be used by site
export APP_ENGINE_SERVICE="backend-q"
python3 build_app_yaml.py
gcloud app deploy --project="${RECAI_PROJECT}"
