curl -X DELETE \
 -H "Authorization: Bearer $(gcloud auth print-access-token recai-predict-sa@babrams-recai-demo.iam.gserviceaccount.com)" \
    "https://recommendationengine.googleapis.com/v1beta1/projects/babrams-recai-demo/locations/global/catalogs/default_catalog/eventStores/default_event_store/predictionApiKeyRegistrations/AIzaSyBM_vZYWD9eNDtlLkiAlZqRJP7HQ-1KxUs"
