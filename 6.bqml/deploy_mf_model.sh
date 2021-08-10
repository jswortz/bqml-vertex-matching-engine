#!/bin/bash

source ../0.setup/env_vars.sh

# Export and run local
#mkdir bqml_testing/
#cd bqml_testing
#gsutil cp -r gs://mf_model_export/ ./
#mkdir -p mf_model/1
#cp -r mf_model_export/mf_model_export/* mf_model/1/
#docker pull tensorflow/serving
#docker run -p 8500:8500 --network="host" --mount type=bind,source=`pwd`/mf_model,target=/models/mf_model -e MODEL_NAME=mf_model -t tensorflow/serving &

# Call for a prediction
#curl -d '{"instances": [{"visitorId": "123"}]}' -X POST http://localhost:8501/v1/models/mf_model:predict

# Build and deploy for online predictions
export MODEL_DIR="gs://${RECAI_PROJECT}_model_exports/${BQML_NAME}/"
bq extract -m css_retail."${BQML_NAME}" "${MODEL_DIR}"

gcloud ai-platform models create --region="${PRIMARY_REGION}" "${BQML_NAME}"

export VERSION_NAME="v1"
export FRAMEWORK="TENSORFLOW"
gcloud ai-platform versions create "${VERSION_NAME}" \
--model="${BQML_NAME}" --origin="${MODEL_DIR}" \
--runtime-version=1.15 --framework="${FRAMEWORK}" \
--region="${PRIMARY_REGION}"
# Need to do service account access on bucket

# describe model
gcloud ai-platform versions describe "${VERSION_NAME}" \
--model "${BQML_NAME}"

