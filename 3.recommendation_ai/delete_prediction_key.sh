#!/bin/bash

source ../0.setup/env_vars.sh

API_KEY=AIzaSyBM_vZYWD9eNDtlLkiAlZqRJP7HQ-1KxUs

curl -X DELETE \
 -H "Authorization: Bearer $(gcloud auth print-access-token ${RECAI_SA}@${RECAI_PROJECT}.iam.gserviceaccount.com)" \
    "https://recommendationengine.googleapis.com/v1beta1/projects/${RECAI_PROJECT}/locations/global/catalogs/default_catalog/eventStores/default_event_store/predictionApiKeyRegistrations/${API_KEY}"
