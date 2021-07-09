curl -X POST \
 -H "Authorization: Bearer $(gcloud auth print-access-token recai-predict-sa@babrams-recai-demo.iam.gserviceaccount.com)" \
 -H "Content-Type: application/json; charset=utf-8" \
 --data "{
       "predictionApiKeyRegistration": {
            "apiKey": '877ee0585a818cae79bd1e43475347a74ec397bc'
        }
    }" "https://recommendationengine.googleapis.com/v1beta1/projects/babrams-recai-demo/locations/global/catalogs/default_catalog/eventStores/default_event_store/predictionApiKeyRegistrations"
