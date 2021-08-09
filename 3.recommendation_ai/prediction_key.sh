#!/bin/bash

source ../0.setup/env_vars.sh

curl -X POST \
 -H "Authorization: Bearer $(gcloud auth print-access-token ${RECAI_SA}@${RECAI_PROJECT}.iam.gserviceaccount.com)" \
 -H "Content-Type: application/json; charset=utf-8" \
 --data '{"predictionApiKeyRegistration": {"apiKey": "'${PREDICT_KEY}'"}}' \
 "https://recommendationengine.googleapis.com/v1beta1/projects/${RECAI_PROJECT}/locations/global/catalogs/default_catalog/eventStores/default_event_store/predictionApiKeyRegistrations"
