#!/bin/bash

source ../0.setup/env_vars.sh

PROJECT_NUMBER=$(gcloud projects describe "${RECAI_PROJECT}" | grep projectNumber | cut -d\' -f2)
export PROJECT_NUMBER

CLOUD_SQL_IP=$(gcloud sql instances describe pso-css-retail | grep -i ipAddress: | cut -d: -f2 | cut -d" " -f2)
export CLOUD_SQL_IP

export LOADER_KEY="AIzaSyAZANO4X3DYLtK1KD15T9I7VufKgJabNvY"
export PREDICT_KEY="AIzaSyC0dJDDRkgX0bui8GFqwFqZdLiC_yQH5nw" # Update this
export OAUTH_CLIENT="371922342503-p4sjpo0kc7emoeesodou8kqsv8dnhem6.apps.googleusercontent.com" # Update this
export OAUTH_KEY="lwfhDWxWrZ6SEAgtkwVpHrcs" # Update this

export GTM_CONTAINER_ID='GTM-W3FXLZ6' # Update this