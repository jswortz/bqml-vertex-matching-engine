#!/bin/bash

source ../0.setup/env_vars.sh

python build_deployment_yaml.py

ng build

gcloud app deploy --project="${RECAI_PROJECT}"

gcloud app deploy --project="${RECAI_PROJECT}" dispatch.yaml
