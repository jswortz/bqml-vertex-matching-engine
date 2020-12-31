gcloud builds submit --tag gcr.io/css-storeops/retail-store --project css-storeops
gcloud run deploy --image gcr.io/css-storeops/retail-store --project css-storeops --platform managed
retail-store
18