curl -X POST \
 -H "Authorization: Bearer $(gcloud auth print-access-token YOUR-SERVICE-ACCOUNT)" \
 -H "Content-Type: application/json; charset=utf-8" \
 --data "{
       "predictionApiKeyRegistration": {
            "apiKey": 'API-KEY'
        }
    }" "https://recommendationengine.googleapis.com/v1beta1/projects/PROJECT-ID/locations/global/catalogs/default_catalog/eventStores/default_event_store/predictionApiKeyRegistrations"
