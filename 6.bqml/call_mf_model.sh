#!/bin/bash

source ../0.setup/env_vars.sh

# call online model
#export INPUT_DATA_FILE="./instances.json"
#printf '{"visitorId": "123"}\n{"visitorId": "19284"}\n{"visitorId": "9876"}' > "${INPUT_DATA_FILE}"
#gcloud ai-platform predict --model "${BQML_NAME}" \
#--version "${VERSION_NAME}" --json-instances "${INPUT_DATA_FILE}" \
#--region=us-central1

export PREDICT_SA="babrams@google.com"
# Curl version
curl -H "Content-Type: application/json; charset=utf-8" -H "Authorization: Bearer $(gcloud auth print-access-token "${PREDICT_SA}")" -X POST "https://${REGION}-ml.googleapis.com/v1/projects/${RECAI_PROJECT}/models/${BQML_NAME}/versions/v1:predict" --data '{"instances": [{"visitorId":"123"}]}'

#quick load test
#ctr=0
#while [ $ctr -lt 100 ];do
#  echo ${ctr}
#  curl -H "Content-Type: application/json; charset=utf-8" -H "Authorization: Bearer $(gcloud auth print-access-token babrams@google.com)" -X POST "https://us-central1-ml.googleapis.com/v1/projects/babrams-recai-demo/models/mf_model/versions/v1:predict" --data '{"instances": [{"visitorId":"'${RANDOM}'"}]}' > /dev/null 2>&1
#  ctr=$((ctr + 1))
#done
