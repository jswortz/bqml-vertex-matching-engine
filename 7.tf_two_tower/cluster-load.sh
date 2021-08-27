#!/bin/bash
#BUCKET=actions-bucket-jw
#REGION=us-central1
#CLUSTER_NAME=tf-clus
#gcloud dataproc clusters create ${CLUSTER_NAME} \
#    --region ${REGION} \
#    --master-machine-type n1-standard-16 \
#    --worker-machine-type n1-highmem-16 \
#    --master-accelerator type=nvidia-tesla-t4 \
#    --worker-accelerator type=nvidia-tesla-t4 \
#    --image-version preview-ubuntu18 \
#    --metadata include-gpus=true \
#    --metadata gpu-driver-provider=NVIDIA \
#    --metadata init-actions-repo=gs://${BUCKET} \
#    --optional-components JUPYTER \
#    --initialization-actions gs://${BUCKET}/mlvm/mlvm.sh \
#    --initialization-action-timeout=45m \
#    --enable-component-gateway