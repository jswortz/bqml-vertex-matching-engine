#!/bin/bash

source ../0.setup/env_vars.sh

# Set catalog level
curl -X PATCH \
-H "Authorization: Bearer $(gcloud auth print-access-token "${PREDICT_SA}")" \
-H "Content-Type: application/json; charset=utf-8" \
--data '{
"catalogItemLevelConfig": {
"eventItemLevel": "MASTER",
"predictItemLevel": "MASTER"
}
}' \
"https://recommendationengine.googleapis.com/v1beta1/projects/${RECAI_PROJECT}/locations/global/catalogs/default_catalog"

# Load data from Big Query
curl -X POST \
-H "Authorization: Bearer $(gcloud auth print-access-token "${PREDICT_SA}")" \
-H "Content-Type: application/json; charset=utf-8" \
--data '{
"inputConfig":{
"bigQuerySource": {
  "datasetId":"css_retail",
  "tableId":"recommendation_ai_data",
  "dataSchema":"catalog_recommendation_ai"
}
}
}' \
"https://recommendationengine.googleapis.com/v1beta1/projects/${RECAI_PROJECT}/locations/global/catalogs/default_catalog/catalogItems:import"


curl -H "Authorization: Bearer $(gcloud auth print-access-token "${PREDICT_SA}")" \
"https://recommendationengine.googleapis.com/v1beta1/projects/${RECAI_PROJECT}/locations/global/catalogs/default_catalog/operations/"


#export GOOGLE_APPLICATION_CREDENTIALS=/tmp/my-key.json
for page_type in "home_page_view" "detail_page_view" "add_to_cart" "purchase_complete"; do
  curl -v -X POST -H "Content-Type: application/json; charset=utf-8" \
  -H "Authorization: Bearer $(gcloud auth print-access-token "${PREDICT_SA}")" \
  "https://recommendationengine.googleapis.com/v1beta1/projects/${RECAI_PROJECT}/locations/global/catalogs/default_catalog/userEvents:import" \
    --data '{
      "inputConfig": {
        "bigQuerySource": {
          "datasetId": "css_retail",
          "tableId": "'${page_type}'",
          "dataSchema": "user_events_recommendations_ai"
      }
    }
  }'
done