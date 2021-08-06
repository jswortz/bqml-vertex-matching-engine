#!/bin/bash

PROJECT=babrams-recai-demo
SA=recai-predict-sa
API_KEY=AIzaSyBM_vZYWD9eNDtlLkiAlZqRJP7HQ-1KxUs

curl -X DELETE \
 -H "Authorization: Bearer $(gcloud auth print-access-token ${SA}@${PROJECT}.iam.gserviceaccount.com)" \
    "https://recommendationengine.googleapis.com/v1beta1/projects/${PROJECT}/locations/global/catalogs/default_catalog/eventStores/default_event_store/predictionApiKeyRegistrations/${API_KEY}"
