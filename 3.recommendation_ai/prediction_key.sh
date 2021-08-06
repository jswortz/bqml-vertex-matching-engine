#!/bin/bash

PROJECT=babrams-recai-demo
SA=recai-predict-sa
API_KEY=877ee0585a818cae79bd1e43475347a74ec397bc

curl -X POST \
 -H "Authorization: Bearer $(gcloud auth print-access-token ${SA}@${PROJECT}.iam.gserviceaccount.com)" \
 -H "Content-Type: application/json; charset=utf-8" \
 --data "{
       "predictionApiKeyRegistration": {
            "apiKey": '${API_KEY}'
        }
    }" "https://recommendationengine.googleapis.com/v1beta1/projects/${PROJECT}/locations/global/catalogs/default_catalog/eventStores/default_event_store/predictionApiKeyRegistrations"
