curl -X POST \
 -H "Authorization: Bearer $(gcloud auth print-access-token YOUR-SERVICE-ACCOUNT)" \ #update with your service account
 -H "Content-Type: application/json; charset=utf-8" \
 --data "{
       "predictionApiKeyRegistration": {
            "apiKey": 'API-KEY' # update with your api-key
        }
    }"
 "https://recommendationengine.googleapis.com/v1beta1/projects/css-storeops/locations/global/catalogs/default_catalog/eventStores/default_event_store/predictionApiKeyRegistrations"
