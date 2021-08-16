#!/bin/bash

source ../0.setup/env_vars.sh

python build_deployment_yaml.py

gcloud builds submit --tag gcr.io/css-storeops/retail-store \
--project "${RECAI_PROJECT}"
gcloud run deploy --image gcr.io/css-storeops/retail-store \
--project "${RECAI_PROJECT}" --platform managed
