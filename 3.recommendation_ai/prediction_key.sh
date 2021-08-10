#!/bin/bash

source ../0.setup/env_vars.sh

#export LOADER_KEY=AIzaSyAZANO4X3DYLtK1KD15T9I7VufKgJabNvY
#export PREDICT_KEY=AIzaSyAptd6M3SUokdQKMgCAssv-adCOP7fO8s8

curl -X POST \
 -H "Authorization: Bearer $(gcloud auth print-access-token ${RECAI_SA}@${RECAI_PROJECT}.iam.gserviceaccount.com)" \
 -H "Content-Type: application/json; charset=utf-8" \
 --data '{"predictionApiKeyRegistration": {"apiKey": "'${PREDICT_KEY}'"}}' \
 "https://recommendationengine.googleapis.com/v1beta1/projects/${RECAI_PROJECT}/locations/global/catalogs/default_catalog/eventStores/default_event_store/predictionApiKeyRegistrations"
